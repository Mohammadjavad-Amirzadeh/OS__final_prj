import sys
from queue import PriorityQueue

    
def get_autorized_tasks_list(waiting_queue: PriorityQueue, remained_sub1_resource1: int, remained_sub1_resource2: int):
    authorized_tasks = []
    for _, task in list(self.Waiting_queue.queue):
        if task.resource1_usage < remained_sub1_resource1 and task.resource2_usage < remained_sub1_resource2:
            authorized_tasks.append(task)
            remained_sub1_resource1 -= task.resource1_usage
            remained_sub1_resource2 -= task.resource2_usage
    return authorized_tasks
    
def load_balancing(ready_queue1: list, ready_queue2: list, ready_queue3: list) -> list:
    if len(ready_queue1) == 0:
        return ready_queue1
    elif len(ready_queue2) == 0:
        return ready_queue2
    elif len(ready_queue3) == 0:
        return ready_queue3
    
    ready_queue1_time = 0
    for task in ready_queue1:
        ready_queue1_time += task.get_remaining_execution_time()
    ready_queue2_time = 0
    for task in ready_queue2:
        ready_queue1_time += task.get_remaining_execution_time()
    ready_queue3_time = 0
    for task in ready_queue3:
        ready_queue1_time += task.get_remaining_execution_time()
        
    min_time_queue = min(ready_queue1_time, ready_queue2_time, ready_queue3_time)
    
    if min_time_queue == ready_queue1_time:
        return ready_queue1
    elif min_time_queue == ready_queue2_time:
        return ready_queue2
    elif min_time_queue == ready_queue3_time:
        return ready_queue3
    

def long_term_schedular(waiting_queue: PriorityQueue, ready_queue1: list, ready_queue2: list, ready_queue3: list, remained_sub1_resource1: int, remained_sub1_resource2: int):
    authorized_tasks = get_autorized_tasks_list()
    for task in authorized_tasks:
        best_ready_queue = load_balancing(ready_queue1, ready_queue2, ready_queue3)
        if best_ready_queue == ready_queue1:
            ready_queue1.append(task)
        elif best_ready_queue == ready_queue2:
            ready_queue2.append(task)
        elif best_ready_queue == ready_queue3:
            ready_queue3.append(task)
    return ready_queue1, ready_queue2, ready_queue3
    
    
