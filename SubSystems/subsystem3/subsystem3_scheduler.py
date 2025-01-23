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
    """Implement Rate Monotonic scheduling"""
    if not ready_queue:
        return None, None
    
    # Sort by period - shortest period gets highest priority
    # 1/period would give us priority, so sorting by period directly gives same result
    ready_tasks = [task for task in ready_queue if task.repetitions_number > 0]
    if not ready_tasks:
        return None, None
        
    selected_task = min(ready_tasks, key=lambda x: x.period)
    next_deadline = get_next_deadline(selected_task, current_time)
    
    if selected_task.get_remaining_execution_time() > 0:
        return selected_task, next_deadline
            
    return None, None

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
