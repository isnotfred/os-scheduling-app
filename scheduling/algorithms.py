"""
CPU Scheduling Algorithms Implementation
Includes: FCFS, SJF, Priority, HRRN, SRTF, Preemptive Priority, and RR Scheduling

Args of each algorithm:
    processes: List of process objects
    processes_count: Number of processes
"""

def execute_process(process, current_time):
    """Execute a non-preemptive process and calculate its timing metrics."""
    process.starting_time = current_time
    current_time += process.burst_time
    process.completion_time = current_time
    process.turnaround_time = process.completion_time - process.arrival_time
    process.waiting_time = process.turnaround_time - process.burst_time
    process.response_time = process.starting_time - process.arrival_time
    process.completed = True
    return current_time


# ------------------ Non-Preemptive Scheduling ------------------

def first_come_first_serve(processes, processes_count):
    """
    First Come First Serve (FCFS) Scheduling Algorithm.
    Non-preemptive scheduling based on arrival time.
    """
    completed_count = 0
    current_time = 0
    gantt_chart = []
    last_pid = None

    while completed_count < processes_count:
        selected_index = -1
        earliest_arrival = float('inf')
        for i, process in enumerate(processes):
            if process.arrival_time <= current_time and not process.completed:
                if process.arrival_time < earliest_arrival or \
                   (process.arrival_time == earliest_arrival and process.pid < processes[selected_index].pid):
                    selected_index = i
                    earliest_arrival = process.arrival_time

        if selected_index == -1:
            if last_pid != "IDLE":
                gantt_chart.append((current_time, None))
                last_pid = "IDLE"
            current_time += 1
            continue

        process = processes[selected_index]

        if last_pid != process.pid:
            gantt_chart.append((current_time, f"P{process.pid}"))
            last_pid = process.pid

        current_time = execute_process(process, current_time)
        completed_count += 1

    gantt_chart.append((current_time, "END"))
    return gantt_chart


def shortest_job_first(processes, processes_count):
    """
    Shortest Job First (SJF) Scheduling Algorithm.
    Non-preemptive scheduling based on burst time.
    """
    completed_count = 0
    current_time = 0
    gantt_chart = []
    last_pid = None

    while completed_count < processes_count:
        selected_index = -1
        shortest_burst = float('inf')
        for i, process in enumerate(processes):
            if process.arrival_time <= current_time and not process.completed:
                if process.burst_time < shortest_burst or \
                   (process.burst_time == shortest_burst and (
                       process.arrival_time < processes[selected_index].arrival_time or
                       (process.arrival_time == processes[selected_index].arrival_time and
                        process.pid < processes[selected_index].pid))):
                    selected_index = i
                    shortest_burst = process.burst_time

        if selected_index == -1:
            if last_pid != "IDLE":
                gantt_chart.append((current_time, None))
                last_pid = "IDLE"
            current_time += 1
            continue

        process = processes[selected_index]

        if last_pid != process.pid:
            gantt_chart.append((current_time, f"P{process.pid}"))
            last_pid = process.pid

        current_time = execute_process(process, current_time)
        completed_count += 1

    gantt_chart.append((current_time, "END"))
    return gantt_chart


def non_preemptive_priority(processes, processes_count):
    """
    Non-Preemptive Priority Scheduling Algorithm.
    Non-preemptive scheduling based on priority level.
    """
    completed_count = 0
    current_time = 0
    gantt_chart = []
    last_pid = None

    while completed_count < processes_count:
        selected_index = -1
        highest_priority = float('inf')
        for i, process in enumerate(processes):
            if process.arrival_time <= current_time and not process.completed:
                if process.priority < highest_priority or \
                   (process.priority == highest_priority and (
                       process.arrival_time < processes[selected_index].arrival_time or
                       (process.arrival_time == processes[selected_index].arrival_time and (
                           process.burst_time < processes[selected_index].burst_time or
                           (process.burst_time == processes[selected_index].burst_time and
                            process.pid < processes[selected_index].pid)
                       ))
                   )):
                    selected_index = i
                    highest_priority = process.priority

        if selected_index == -1:
            if last_pid != "IDLE":
                gantt_chart.append((current_time, None))
                last_pid = "IDLE"
            current_time += 1
            continue

        process = processes[selected_index]

        if last_pid != process.pid:
            gantt_chart.append((current_time, f"P{process.pid}"))
            last_pid = process.pid

        current_time = execute_process(process, current_time)
        completed_count += 1

    gantt_chart.append((current_time, "END"))
    return gantt_chart


def highest_response_ratio_next(processes, processes_count):
    """
    Highest Response Ratio Next (HRRN) Scheduling Algorithm.
    Non-preemptive scheduling that favors both short jobs and long-waiting jobs.
    """
    completed_count = 0
    current_time = 0
    gantt_chart = []
    last_pid = None

    while completed_count < processes_count:
        selected_index = -1
        highest_ratio = -1

        for i, process in enumerate(processes):
            if not process.completed and process.arrival_time <= current_time:
                waiting_time = current_time - process.arrival_time
                response_ratio = (waiting_time + process.burst_time) / process.burst_time

                if response_ratio > highest_ratio or \
                   (response_ratio == highest_ratio and (
                       process.arrival_time < processes[selected_index].arrival_time or
                       (process.arrival_time == processes[selected_index].arrival_time and (
                           process.burst_time < processes[selected_index].burst_time or
                           (process.burst_time == processes[selected_index].burst_time and
                            process.pid < processes[selected_index].pid)
                       ))
                   )):
                    selected_index = i
                    highest_ratio = response_ratio

        if selected_index == -1:
            if last_pid != "IDLE":
                gantt_chart.append((current_time, None))
                last_pid = "IDLE"
            current_time += 1
            continue

        process = processes[selected_index]

        if last_pid != process.pid:
            gantt_chart.append((current_time, f"P{process.pid}"))
            last_pid = process.pid

        current_time = execute_process(process, current_time)
        completed_count += 1

    gantt_chart.append((current_time, "END"))
    return gantt_chart


# ------------------ Preemptive Scheduling ------------------

def shortest_remaining_time_first(processes, processes_count):
    """
    Shortest Remaining Time First (SRTF) Scheduling Algorithm.
    Executes shortest remaining time process at each time unit.
    Supports process preemption when shorter remaining time process arrives.
    """
    current_time = 0
    completed_count = 0
    gantt_chart = []
    last_pid = None

    while completed_count < processes_count:
        selected_index = -1
        shortest_remaining = float('inf')
        for i, process in enumerate(processes):
            if process.arrival_time <= current_time and not process.completed:
                if process.remaining_time < shortest_remaining or \
                   (process.remaining_time == shortest_remaining and (
                       process.arrival_time < processes[selected_index].arrival_time or
                       (process.arrival_time == processes[selected_index].arrival_time and
                        process.pid < processes[selected_index].pid)
                   )):
                    selected_index = i
                    shortest_remaining = process.remaining_time

        if selected_index == -1:
            if last_pid != "IDLE":
                gantt_chart.append((current_time, None))
                last_pid = "IDLE"
            current_time += 1
            continue

        process = processes[selected_index]

        if process.starting_time == -1:
            process.starting_time = current_time
            process.response_time = current_time - process.arrival_time

        if last_pid != process.pid:
            gantt_chart.append((current_time, f"P{process.pid}"))
            last_pid = process.pid

        process.remaining_time -= 1
        current_time += 1

        if process.remaining_time == 0:
            process.completed = True
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            completed_count += 1

    gantt_chart.append((current_time, "END"))
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
    last_pid = None

    while completed_count < processes_count:
        selected_index = -1
        highest_priority = float('inf')

        for i, process in enumerate(processes):
            if process.arrival_time <= current_time and not process.completed:
                if process.priority < highest_priority or \
                   (process.priority == highest_priority and (
                       process.arrival_time < processes[selected_index].arrival_time or
                       (process.arrival_time == processes[selected_index].arrival_time and (
                           process.burst_time < processes[selected_index].burst_time or
                           (process.burst_time == processes[selected_index].burst_time and
                            process.pid < processes[selected_index].pid)
                       ))
                   )):
                    selected_index = i
                    highest_priority = process.priority

        if selected_index == -1:
            if last_pid != "IDLE":
                gantt_chart.append((current_time, None))
                last_pid = "IDLE"
            current_time += 1
            continue

        process = processes[selected_index]

        if process.starting_time == -1:
            process.starting_time = current_time
            process.response_time = current_time - process.arrival_time

        if last_pid != process.pid:
            gantt_chart.append((current_time, f"P{process.pid}"))
            last_pid = process.pid

        process.remaining_time -= 1
        current_time += 1

        if process.remaining_time == 0:
            process.completed = True
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            completed_count += 1

    gantt_chart.append((current_time, "END"))
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
    last_pid = None

    ready_queue = []
    arrived = [False] * processes_count
    
    while completed_count < processes_count:
        # Add newly arrived processes to ready queue
        for i, process in enumerate(processes):
            if not arrived[i] and process.arrival_time <= current_time and not process.completed:
                ready_queue.append(i)
                arrived[i] = True

        if not ready_queue:
            if last_pid != "IDLE":
                gantt_chart.append((current_time, None))
                last_pid = "IDLE"
            current_time += 1
            continue

        idx = ready_queue.pop(0)
        process = processes[idx]

        if process.starting_time == -1:
            process.starting_time = current_time
            process.response_time = current_time - process.arrival_time

        if last_pid != process.pid:
            gantt_chart.append((current_time, f"P{process.pid}"))
            last_pid = process.pid

        execution_time = min(time_quantum, process.remaining_time)
        process.remaining_time -= execution_time
        current_time += execution_time

        # Add processes that arrived during execution
        for i, p in enumerate(processes):
            if not arrived[i] and p.arrival_time <= current_time and not p.completed:
                ready_queue.append(i)
                arrived[i] = True

        if process.remaining_time == 0:
            process.completed = True
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            completed_count += 1
        else:
            ready_queue.append(idx)
        
    gantt_chart.append((current_time, "END"))
    return gantt_chart


# ------------------ Metrics ------------------

def calculate_averages(processes, processes_count):
    """
    Calculate average turnaround time, waiting time, and response time.
    
    Returns:
        dict: Contains turnaround_time_avg, waiting_time_avg, response_time_avg
    """
    total_tat = sum(p.turnaround_time for p in processes)
    total_wt = sum(p.waiting_time for p in processes)
    total_rt = sum(p.response_time for p in processes)

    return {
        "turnaround_time_avg": total_tat / processes_count,
        "waiting_time_avg": total_wt / processes_count,
        "response_time_avg": total_rt / processes_count
    }
