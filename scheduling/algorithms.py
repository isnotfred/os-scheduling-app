# Finds the process with highest response ratio
def find_highest_response_ratio(processes, current_time):
    highest_ratio = -1
    selected_index = -1
    
    for i, process in enumerate(processes):
        # Only check the processes who has already arrived
        if not process.completed and process.arrival_time <= current_time:
            ratio = ((current_time - process.arrival_time) + process.burst_time) / process.burst_time

            # Check if the process' ratio is higher than highest ratio
            if ratio > highest_ratio:
                highest_ratio = ratio
                selected_index = i
            elif ratio == highest_ratio:
            # Tie-breaker 1: earlier arrival time
                if process.arrival_time < processes[selected_index].arrival_time:
                    selected_index = i
                # Tie-breaker 2: lower PID
                elif process.arrival_time == processes[selected_index].arrival_time:
                    if process.pid < processes[selected_index].pid:
                        selected_index = i

    return selected_index

# HRRN Scheduling
def highest_response_ratio_next(processes, processes_count):
    total_processes = processes_count
    completed_count = current_time = 0
    gantt_chart = []

    while completed_count < total_processes:
        index = find_highest_response_ratio(processes, current_time)

        # Move time if there are no processes available
        if index == -1:
            current_time += 1
        # Complete process with the highest response ratio
        else:
            gantt_chart.append((current_time, f"P{processes[index].pid}"))
            processes[index].starting_time = current_time
            current_time += processes[index].burst_time
            processes[index].completion_time = current_time
            processes[index].turnaround_time = current_time - processes[index].arrival_time
            processes[index].waiting_time = processes[index].turnaround_time - processes[index].burst_time
            processes[index].response_time = processes[index].starting_time - processes[index].arrival_time
            processes[index].completed = True
            completed_count += 1

    gantt_chart.append((current_time, None))

    return gantt_chart

# Preemptive Priority Scheduling
def preemptive_priority(processes, processes_count):
    current_time = 0
    completed_count = 0
    gantt_chart = []
    last_pid = -1
    current_process_index = -1

    while completed_count < processes_count:
        # Find process with highest priority (lowest priority number)
        highest_priority_index = -1
        highest_priority = float('inf')
        
        for i, process in enumerate(processes):
            if (process.arrival_time <= current_time and 
                not process.completed and 
                process.priority < highest_priority):
                highest_priority = process.priority
                highest_priority_index = i
            elif (process.arrival_time <= current_time and 
                  not process.completed and 
                  process.priority == highest_priority):
                # Tie-breaker 0: Prefer currently running process (minimize context switches)
                if i == current_process_index:
                    highest_priority_index = i
                elif highest_priority_index == current_process_index:
                    continue  # Keep current process
                # Tie-breaker 1: earlier arrival time
                elif process.arrival_time < processes[highest_priority_index].arrival_time:
                    highest_priority_index = i
                # Tie-breaker 2: shorter burst time
                elif process.arrival_time == processes[highest_priority_index].arrival_time:
                    if process.burst_time < processes[highest_priority_index].burst_time:
                        highest_priority_index = i
                    # Tie-breaker 3: lower process id        
                    elif process.burst_time == processes[highest_priority_index].burst_time:
                        if process.pid < processes[highest_priority_index].pid:
                            highest_priority_index = i

        if highest_priority_index == -1:
            current_time += 1
            current_process_index = -1
            continue

        process = processes[highest_priority_index]
        current_process_index = highest_priority_index
        
        # Set starting time if first execution
        if process.starting_time == -1:
            process.starting_time = current_time
            process.response_time = current_time - process.arrival_time

        # Add to gantt chart if different from last process
        if process.pid != last_pid:
            gantt_chart.append((current_time, f"P{process.pid}"))
            last_pid = process.pid

        # Execute for 1 time unit
        process.remaining_time -= 1
        current_time += 1

        # Check if process completed
        if process.remaining_time == 0:
            process.completed = True
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            completed_count += 1
            current_process_index = -1

    gantt_chart.append((current_time, None))
    return gantt_chart

# Calculates the averages of TAT, WT, RT
def calculate_averages(processes, processes_count):
    turnaround_time_total = waiting_time_total = response_time_total = 0

    for process in processes:
        turnaround_time_total += process.turnaround_time
        waiting_time_total += process.waiting_time
        response_time_total += process.response_time

    return {"turnaround_time_avg": turnaround_time_total / processes_count,
            "waiting_time_avg": waiting_time_total / processes_count,
            "response_time_avg": response_time_total / processes_count}