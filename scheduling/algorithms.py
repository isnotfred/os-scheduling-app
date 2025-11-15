"""
CPU Scheduling Algorithms Implementation
Includes: FCFS, SJF, Priority, HRRN, SRTF, Preemptive Priority, and RR Scheduling

Args of each algorithm:
    processes: List of process objects
    processes_count: Number of processes
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
                    elif process.arrival_time == processes[selected_index].arrival_time:
                        # Tie-breaker 2: shorter burst time
                        if process.burst_time < processes[selected_index].burst_time:
                            selected_index = i
                        # Tie-breaker 3: lower PID
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

def shortest_remaining_time_first(processes, processes_count):
    """
    Shortest Remaining Time First (SRTF) Scheduling Algorithm.
    Executes shortest remaining time process at each time unit.
    Supports process preemption when shorter remaining time process arrives.
    """
    current_time = 0
    completed_count = 0
    gantt_chart = []
    last_pid = -1
    current_process_index = -1

    while completed_count < processes_count:
        # Find process with shortest remaining time
        selected_index = -1
        shortest_remaining_time = float('inf')
        
        for i, process in enumerate(processes):
            if process.arrival_time <= current_time and not process.completed:
                if process.remaining_time < shortest_remaining_time:
                    selected_index = i
                    shortest_remaining_time = process.remaining_time
                elif process.remaining_time == shortest_remaining_time:
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
                    # Tie-breaker 1: earlier arrival time
                    if process.arrival_time < processes[selected_index].arrival_time:
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

def round_robin(processes, processes_count, time_quantum):
    """
    Round Robin (RR) Scheduling Algorithm.
    Preemptive scheduling where each process gets a fixed time quantum in circular order.
    
    Added Args:
        time_quantum: Time slice allocated to each process
    """
    current_time = 0
    completed_count = 0
    gantt_chart = []
    last_pid = -1
    
    # Create ready queue - processes ordered by arrival, then PID
    ready_queue = []
    processes_copy = sorted(enumerate(processes), key=lambda x: (x[1].arrival_time, x[1].pid))
    next_process_idx = 0
    
    while completed_count < processes_count:
        # Add newly arrived processes to ready queue
        while next_process_idx < processes_count:
            idx, process = processes_copy[next_process_idx]
            if process.arrival_time <= current_time and not process.completed:
                if idx not in [p[0] for p in ready_queue]:
                    ready_queue.append((idx, process))
                    next_process_idx += 1
            else:
                break
        
        # No process in ready queue, advance time
        if not ready_queue:
            current_time += 1
            continue
        
        # Get process from front of queue
        selected_index, process = ready_queue.pop(0)
        
        # Set starting time on first execution
        if process.starting_time == -1:
            process.starting_time = current_time
            process.response_time = current_time - process.arrival_time
        
        # Add to gantt chart when process changes
        if process.pid != last_pid:
            gantt_chart.append((current_time, f"P{process.pid}"))
            last_pid = process.pid
        
        # Execute for time quantum or until completion
        execution_time = min(time_quantum, process.remaining_time)
        process.remaining_time -= execution_time
        current_time += execution_time
        
        # Add newly arrived processes to ready queue during execution
        while next_process_idx < processes_count:
            idx, proc = processes_copy[next_process_idx]
            if proc.arrival_time <= current_time and not proc.completed:
                if idx not in [p[0] for p in ready_queue] and idx != selected_index:
                    ready_queue.append((idx, proc))
                    next_process_idx += 1
            else:
                break
        
        # Check if process completed
        if process.remaining_time == 0:
            process.completed = True
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            completed_count += 1
        else:
            # Process not completed, add back to end of ready queue
            ready_queue.append((selected_index, process))
    
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