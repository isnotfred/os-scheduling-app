"""
CPU Scheduling Algorithms Implementation
Includes: FCFS, SJF, Priority, HRRN, and Preemptive Priority Scheduling
"""

def execute_process(process, current_time):
    """Execute a process and calculate its timing metrics."""
    process.starting_time = current_time
    current_time += process.burst_time
    process.completion_time = current_time
    process.turnaround_time = process.completion_time - process.arrival_time
    process.waiting_time = process.turnaround_time - process.burst_time
    process.response_time = process.starting_time - process.arrival_time
    process.completed = True
    return current_time


def first_come_first_serve(processes, processes_count):
    """
    First Come First Serve (FCFS) Scheduling Algorithm.
    Non-preemptive scheduling based on arrival time.
    """
    completed_count = 0
    current_time = 0
    gantt_chart = []

    while completed_count < processes_count:
        # Find earliest arrived process that hasn't completed
        selected_index = -1
        earliest_arrival = float('inf')

        for i, process in enumerate(processes):
            if process.arrival_time <= current_time and not process.completed:
                if process.arrival_time < earliest_arrival:
                    selected_index = i
                    earliest_arrival = process.arrival_time
                elif process.arrival_time == earliest_arrival:
                    # Tie-breaker: lower PID
                    if process.pid < processes[selected_index].pid:
                        selected_index = i

        # No process available, advance time
        if selected_index == -1:
            current_time += 1
            continue
        
        # Execute selected process
        process = processes[selected_index]
        gantt_chart.append((current_time, f"P{process.pid}"))
        current_time = execute_process(process, current_time)
        completed_count += 1

    gantt_chart.append((current_time, None))
    return gantt_chart


def shortest_job_first(processes, processes_count):
    """
    Shortest Job First (SJF) Scheduling Algorithm.
    Non-preemptive scheduling based on burst time.
    """
    completed_count = 0
    current_time = 0
    gantt_chart = []

    while completed_count < processes_count:
        # Find process with shortest burst time
        selected_index = -1
        shortest_burst = float('inf')

        for i, process in enumerate(processes):
            if process.arrival_time <= current_time and not process.completed:
                if process.burst_time < shortest_burst:
                    selected_index = i
                    shortest_burst = process.burst_time
                elif process.burst_time == shortest_burst:
                    # Tie-breaker 1: earlier arrival time
                    if process.arrival_time < processes[selected_index].arrival_time:
                        selected_index = i
                    # Tie-breaker 2: lower PID
                    elif process.arrival_time == processes[selected_index].arrival_time:
                        if process.pid < processes[selected_index].pid:
                            selected_index = i

        # No process available, advance time
        if selected_index == -1:
            current_time += 1
            continue

        # Execute selected process
        process = processes[selected_index]
        gantt_chart.append((current_time, f"P{process.pid}"))
        current_time = execute_process(process, current_time)
        completed_count += 1

    gantt_chart.append((current_time, None))
    return gantt_chart

def non_preemptive_priority(processes, processes_count):
    """
    Non-Preemptive Priority Scheduling Algorithm.
    Non-preemptive scheduling based on priority level.
    """
    completed_count = 0
    current_time = 0
    gantt_chart = []

    while completed_count < processes_count:
        # Find process with shortest burst time
        selected_index = -1
        highest_priority = float('inf')

        for i, process in enumerate(processes):
            if process.arrival_time <= current_time and not process.completed:
                if process.priority < highest_priority:
                    selected_index = i
                    highest_priority = process.priority
                elif process.priority == highest_priority:
                    # Tie-breaker 1: earlier arrival time
                    if process.arrival_time < processes[selected_index].arrival_time:
                        selected_index = i
                    elif process.arrival_time == processes[selected_index].arrival_time:
                        if process.burst_time < processes[selected_index].burst_time:
                            selected_index = i
                        # Tie-breaker 2: lower PID
                        elif process.burst_time == processes[selected_index].burst_time:
                            if process.pid < processes[selected_index].pid:
                                selected_index = i

        # No process available, advance time
        if selected_index == -1:
            current_time += 1
            continue

        # Execute selected process
        process = processes[selected_index]
        gantt_chart.append((current_time, f"P{process.pid}"))
        current_time = execute_process(process, current_time)
        completed_count += 1

    gantt_chart.append((current_time, None))
    return gantt_chart    

def highest_response_ratio_next(processes, processes_count):
    """
    Highest Response Ratio Next (HRRN) Scheduling Algorithm.
    Non-preemptive scheduling that favors both short jobs and long-waiting jobs.
    """
    completed_count = 0
    current_time = 0
    gantt_chart = []

    while completed_count < processes_count:
        highest_ratio = -1
        selected_index = -1
        
        for i, process in enumerate(processes):
            if not process.completed and process.arrival_time <= current_time:
                # Calculate response ratio
                waiting_time = current_time - process.arrival_time
                ratio = (waiting_time + process.burst_time) / process.burst_time

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

        # No process available, advance time
        if selected_index == -1:
            current_time += 1
            continue
        
        # Execute selected process
        process = processes[selected_index]
        gantt_chart.append((current_time, f"P{process.pid}"))
        current_time = execute_process(process, current_time)
        completed_count += 1

    gantt_chart.append((current_time, None))
    return gantt_chart

def preemptive_priority(processes, processes_count):
    """
    Preemptive Priority Scheduling Algorithm.
    Executes highest priority (lowest priority number) process at each time unit.
    Supports process preemption when higher priority process arrives.
    """
    current_time = 0
    completed_count = 0
    gantt_chart = []
    last_pid = -1
    current_process_index = -1

    while completed_count < processes_count:
        # Find process with highest priority (lowest priority number)
        selected_index = -1
        highest_priority = float('inf')
        
        for i, process in enumerate(processes):
            if process.arrival_time <= current_time and not process.completed:
                if process.priority < highest_priority:
                    selected_index = i
                    highest_priority = process.priority
                elif process.priority == highest_priority:
                    # Tie-breaker 0: minimize context switches (prefer current process)
                    if i == current_process_index:
                        selected_index = i
                    elif selected_index == current_process_index:
                        continue
                    # Tie-breaker 1: earlier arrival time
                    elif process.arrival_time < processes[selected_index].arrival_time:
                        selected_index = i
                    # Tie-breaker 2: shorter burst time
                    elif process.arrival_time == processes[selected_index].arrival_time:
                        if process.burst_time < processes[selected_index].burst_time:
                            selected_index = i
                        # Tie-breaker 3: lower PID
                        elif process.burst_time == processes[selected_index].burst_time:
                            if process.pid < processes[selected_index].pid:
                                selected_index = i

        # No process available, advance time
        if selected_index == -1:
            current_time += 1
            current_process_index = -1
            continue
        
        process = processes[selected_index]
        current_process_index = selected_index
        
        # Set starting time on first execution
        if process.starting_time == -1:
            process.starting_time = current_time
            process.response_time = current_time - process.arrival_time

        # Add to gantt chart only when process changes
        if process.pid != last_pid:
            gantt_chart.append((current_time, f"P{process.pid}"))
            last_pid = process.pid

        # Execute for one time unit
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


def calculate_averages(processes, processes_count):
    """
    Calculate average turnaround time, waiting time, and response time.
    
    Returns:
        dict: Contains turnaround_time_avg, waiting_time_avg, response_time_avg
    """
    turnaround_time_total = 0
    waiting_time_total = 0
    response_time_total = 0

    for process in processes:
        turnaround_time_total += process.turnaround_time
        waiting_time_total += process.waiting_time
        response_time_total += process.response_time

    return {
        "turnaround_time_avg": turnaround_time_total / processes_count,
        "waiting_time_avg": waiting_time_total / processes_count,
        "response_time_avg": response_time_total / processes_count
    }
