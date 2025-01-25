import math

def calculate_utilization(tasks):
    """Calculate total CPU utilization for Rate Monotonic"""
    utilization = 0
    for task in tasks:
        utilization += task.execution_time / task.period
    return utilization

def is_schedulable_rm(tasks):
    """Check if tasks are schedulable under Rate Monotonic"""
    n = len(tasks)
    if n == 0:
        return True
    
    # Calculate utilization bound for Rate Monotonic
    utilization_bound = n * (2**(1/n) - 1)
    current_utilization = calculate_utilization(tasks)
    
    return current_utilization <= utilization_bound

def get_next_deadline(task, current_time):
    """Calculate next deadline based on period and arrival time
    
    For example:
    - Task arrives at t=3
    - Period is 5
    - First deadline is 3 + 5 = 8
    - Next deadlines: 13, 18, etc.
    """
    periods_passed = max(0, (current_time - task.arrival_time) // task.period)
    return task.arrival_time + (periods_passed + 1) * task.period

def rate_monotonic_schedule(ready_queue, current_time):
    """Returns task with shortest period (highest priority) and its next deadline"""
    if not ready_queue:
        return None, float('inf')
    
    highest_priority_task = min(ready_queue, key=lambda x: x.period)
    return highest_priority_task, highest_priority_task.next_deadline

def should_preempt(current_task, ready_queue):
    """Check if current task should be preempted by a task in ready queue"""
    if not ready_queue:
        return False
    for task in ready_queue:
        if task.period < current_task.period:  # Rate Monotonic: shorter period = higher priority
            return True
    return False

def needs_speedup(ready_queue, current_time):
    """Determine if tasks need speedup to meet deadlines"""
    if not ready_queue:
        return False
        
    # Calculate time needed vs time available for each task
    for task in ready_queue:
        if task.repetitions_number <= 0:
            continue
            
        next_deadline = get_next_deadline(task, current_time)
        time_until_deadline = next_deadline - current_time
        
        # If any task needs more time than available, speedup is needed
        if task.get_remaining_execution_time() > time_until_deadline:
            return True
            
    return False
