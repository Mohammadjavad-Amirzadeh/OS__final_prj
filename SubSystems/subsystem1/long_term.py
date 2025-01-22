import sys
from queue import PriorityQueue

def get_autorized_tasks_list(waiting_queue: PriorityQueue, remained_sub1_resource1: int, remained_sub1_resource2: int, current_time: int):
    authorized_tasks = []
    waiting_tasks = list(waiting_queue.queue)
    
    # Clear the queue
    while not waiting_queue.empty():
        waiting_queue.get()
    
    # Process each task
    for priority, task in waiting_tasks:
        # Only authorize tasks that have arrived and have sufficient resources
        if (task.arrival_time <= current_time and 
            task.resource1_usage <= remained_sub1_resource1 and 
            task.resource2_usage <= remained_sub1_resource2):
            authorized_tasks.append(task)
            remained_sub1_resource1 -= task.resource1_usage
            remained_sub1_resource2 -= task.resource2_usage
        else:
            # Put back tasks that cannot be authorized
            waiting_queue.put((priority, task))
            
    return authorized_tasks

def load_balancing(ready_queue1: list, ready_queue2: list, ready_queue3: list, task) -> list:
    # First try to assign to the designated processor queue
    if task.processor_number == 1 and len(ready_queue1) == 0:
        return ready_queue1
    elif task.processor_number == 2 and len(ready_queue2) == 0:
        return ready_queue2
    elif task.processor_number == 3 and len(ready_queue3) == 0:
        return ready_queue3
    
    # If designated queue is not empty, find the least loaded queue
    queue_loads = [
        (ready_queue1, sum(t.get_remaining_execution_time() for t in ready_queue1)),
        (ready_queue2, sum(t.get_remaining_execution_time() for t in ready_queue2)),
        (ready_queue3, sum(t.get_remaining_execution_time() for t in ready_queue3))
    ]
    
    return min(queue_loads, key=lambda x: x[1])[0]

def long_term_schedular(waiting_queue: PriorityQueue, ready_queue1: list, ready_queue2: list, ready_queue3: list, 
                       remained_sub1_resource1: int, remained_sub1_resource2: int, current_time: int):
    authorized_tasks = get_autorized_tasks_list(waiting_queue, remained_sub1_resource1, remained_sub1_resource2, current_time)
    
    for task in authorized_tasks:
        best_ready_queue = load_balancing(ready_queue1, ready_queue2, ready_queue3, task)
        if best_ready_queue == ready_queue1:
            ready_queue1.append(task)
        elif best_ready_queue == ready_queue2:
            ready_queue2.append(task)
        elif best_ready_queue == ready_queue3:
            ready_queue3.append(task)
            
    return waiting_queue, ready_queue1, ready_queue2, ready_queue3


