import time
import math
import queue 
import threading
from SubSystems.subsystem1.subsystem1_task import subsystem1_task
from Resources.Resource1 import resource1
from Resources.Resource2 import resource2
from SubSystems.subsystem1.subsystem1_scheduler import weighted_round_robbin
from SubSystems.subsystem1.long_term import long_term_schedular


class subsystem1:
    def __init__(self, subsystem1_tasks, resource1_number, resource2_number):
        self.subsystem_number = 1
        self.processors_count = 3
        self.tasks = subsystem1_tasks
        self.Waiting_queue = queue.PriorityQueue()
        self.storing_all_tasks = queue.PriorityQueue()
        self.Ready_queue1 = []
        self.Ready_queue2 = []
        self.Ready_queue3 = []
        self.resource1_number = resource1_number
        self.resource2_number = resource2_number
        self.reamining_resource1_number = resource1_number
        self.reamining_resource2_number = resource2_number
        self.resource1_list = []
        self.resource2_list = []
        self.initiate_resources()
        self.add_to_storing_all_tasks()
        
        self.processor1_status = False
        self.processor2_status = False
        self.processor3_status = False
        
        self.processor1_busy_time = 0
        self.processor2_busy_time = 0
        self.processor3_busy_time = 0
        
        self.processor1_assigned_task = None
        self.processor2_assigned_task = None
        self.processor3_assigned_task = None
        
        self.processor1_is_ok = False
        self.processor2_is_ok = False
        self.processor3_is_ok = False
        
        self.finished_tasks = []
        
        self.subsystem_did = {'processor1': 'IDLE',
                              'processor2': 'IDLE',
                              'processor3': 'IDLE'}
        
        self.subsystem1_clock = threading.Event()
        self.resource_lock = threading.Lock()
        self.waiting_queue_lock = threading.Lock()
        self.ready_queue_lock = threading.Lock()
        self.current_time = -1  # Add this line to track system time
        
        
    def initiate_resources(self):
        for resource in range(self.resource1_number):
            self.resource1_list.append(resource1(self.subsystem_number))
        for resource in range(self.resource2_number):
            self.resource1_list.append(resource1(self.subsystem_number))
            
    def print_resources_list_status(self):
        with self.lock:
            for resource in self.resource1_list:
                print(f'resource task_id: {resource.task_id}')    
        
    def add_to_storing_all_tasks(self):
        for task in self.tasks:
            self.storing_all_tasks.put((task.arrival_time, task))

    def print_waiting_queue(self):
        print("Waiting Queue:", self.Waiting_queue.qsize())
        for _, task in list(self.Waiting_queue.queue):
            print(f"Task {task.name}, Arrival Time: {task.arrival_time}, State: {task.state}")
            
    def appropriate_ready_queue_for_load_task(self):
        if self.processor1_busy_time == 0:
            return 1
        elif self.processor2_busy_time == 0:
            return 2
        elif self.processor3_busy_time == 0:
            return 3
        
        if len(self.Ready_queue1) == 0:
            return 1
        elif len(self.Ready_queue2) == 0:
            return 2
        elif len(self.Ready_queue3) == 0:
            return 3
        
        ready_queue_loads = [
            sum(t.get_remaining_execution_time() for t in self.Ready_queue1),
            sum(t.get_remaining_execution_time() for t in self.Ready_queue2),
            sum(t.get_remaining_execution_time() for t in self.Ready_queue3)
        ]
        
        return ready_queue_loads.index(min(ready_queue_loads))
    
    def load_balancer(self):
        while not self.Waiting_queue.empty():
            _, task = self.Waiting_queue.get()
            best_ready_queue = self.appropriate_ready_queue_for_load_task()
            if processor_number == 1:
                # print(f"SUBSYSTEM 1 : TASK {task.name} MOVED TO Ready_queue1 By LOAD_BALANCER")
                self.Ready_queue1.append(task)
            elif processor_number == 2:
                # print(f"SUBSYSTEM 1 : TASK {task.name} MOVED TO Ready_queue2 By LOAD_BALANCER")
                self.Ready_queue2.append(task)
            elif processor_number == 3:
                # print(f"SUBSYSTEM 1 : TASK {task.name} MOVED TO Ready_queue3 By LOAD_BALANCER")                
                self.Ready_queue3.append(task)
                
        lists = [self.Ready_queue1, self.Ready_queue2, self.Ready_queue3]

        while True:
            lengths = [len(lst) for lst in lists]
            max_len = max(lengths)
            min_len = min(lengths)

            if max_len - min_len <= 1:
                break
            
            max_index = lengths.index(max_len)
            min_index = lengths.index(min_len)

            element = lists[max_index].pop()
            lists[min_index].append(element)
        
            
    
    def request_task(self, processor_number):
        waiting_list = []
        with self.waiting_queue_lock:
            while not self.Waiting_queue.empty():
                priority, temp_task = self.Waiting_queue.get()
                waiting_list.append((priority, temp_task))
        counter = 0
        if len(waiting_list) > 0:
            for priority, task in waiting_list:
                if counter < 2:
                    if processor_number == 1:
                        print(f"SUBSYSTEM 1 : TASK {task.name} MOVED TO Ready_queue1 FROM WAITING QUEUE BECAUSE READY_QUEUE 1 REQUESTED TASK")
                        self.Ready_queue1.append(task)
                    elif processor_number == 2:
                        print(f"SUBSYSTEM 1 : TASK {task.name} MOVED TO Ready_queue2 FROM WAITING QUEUE BECAUSE READY_QUEUE 2 REQUESTED TASK")
                        self.Ready_queue2.append(task)
                    elif processor_number == 3:
                        print(f"SUBSYSTEM 1 : TASK {task.name} MOVED TO Ready_queue3 FROM WAITING QUEUE BECAUSE READY_QUEUE 3 REQUESTED TASK")                
                        self.Ready_queue3.append(task)
                else:
                    with self.waiting_queue_lock:
                        self.Waiting_queue.put((priority, task))
                
        else:
            print("SUBSYSTEM 1 : NO TASK IN WAITING QUEUE")
            
    def check_add_task_by_arrival_time(self):
        storing_tasks = []
        while not self.storing_all_tasks.empty():
            storing_tasks.append(self.storing_all_tasks.get())
        t1 = False
        t2 = False
        t3 = False
        for arrival, task in storing_tasks:
            if arrival <= self.current_time:
                with self.ready_queue_lock:
                    if task.processor_number == 1:
                        t1 = True
                        self.Ready_queue1.append(task)
                    elif task.processor_number == 2:
                        t2 = True
                        self.Ready_queue2.append(task)
                    elif task.processor_number == 3:
                        t3 = True
                        self.Ready_queue3.append(task)
            else:
                self.storing_all_tasks.put((arrival, task))
        if t1:
            for task in list(self.Ready_queue1):
                print(f'SUBSYSTEM 1 : ARRIVED {task.name} AND ADD {task.name} To Ready_queue1')
        if t2:
            for task in list(self.Ready_queue2):
                print(f'SUBSYSTEM 1 : ARRIVED {task.name} AND ADD {task.name} To Ready_queue2')
        if t3:
            for task in list(self.Ready_queue3):
                print(f'SUBSYSTEM 1 : ARRIVED {task.name} AND ADD {task.name} To Ready_queue3')
            
    def set_clock(self):
        self.current_time += 1  # Add this line to increment time
        self.check_add_task_by_arrival_time()
        if self.current_time != 0 and self.current_time % 5 == 0:
            self.load_balancer()
        self.processor1_status = True
        self.processor2_status = True
        self.processor3_status = True
        
    def is_processores_finished(self):
        return not(self.processor1_status) and not(self.processor2_status) and not(self.processor3_status)
    
    def processor1(self):
        while True:
            if self.processor1_status:
                
                if self.processor1_busy_time > 0: # there is a task that should be run
                    if self.processor1_assigned_task:
                        # EXECUTION
                        self.subsystem_did['processor1'] = self.processor1_assigned_task
                        self.processor1_assigned_task.proceed_executed_time += 1 
                        self.processor1_busy_time -= 1
                        remaining_time = self.processor1_assigned_task.get_remaining_execution_time()
                        if remaining_time <= 0:
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor1_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor1_assigned_task.resource2_usage
                            print(f"SUBSYSTEM 1 : THIS TASK FINISED IN PROCESSOR 1 => {self.processor1_assigned_task} AND GIVE BACK THIS RESOURCES R1 = {self.processor1_assigned_task.resource1_usage}, R2 = {self.processor1_assigned_task.resource2_usage}")
                            self.finished_tasks.append(self.processor1_assigned_task)
                            self.processor1_assigned_task = None
                            self.processor1_busy_time = 0
                        if remaining_time > 0 and self.processor1_busy_time <= 0: # preempt task from processor
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor1_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor1_assigned_task.resource2_usage
                            print(f"SUBSYSTEM 1 : ENDED QUANTUM OF THIS TASK IN PROCESSOR 1 => {self.processor1_assigned_task} AND GIVE BACK THIS RESOURCES R1 = {self.processor1_assigned_task.resource1_usage}, R2 = {self.processor1_assigned_task.resource2_usage}")
                            with self.ready_queue_lock:
                                self.Ready_queue1.append(self.processor1_assigned_task)
                                
                            self.processor1_assigned_task = None
                            self.processor1_busy_time = 0
                            
                elif self.processor1_busy_time <= 0:
                    empty_at_first = False
                    is_pick_task = False
                    pickuped_task = None    
                    with self.ready_queue_lock:
                        if len(self.Ready_queue1) > 0:
                            while len(self.Ready_queue1) > 0 and not is_pick_task: # try to assign task
                                first_task_in_ready_queue = self.Ready_queue1.pop(0)
                                with self.resource_lock:
                                    if first_task_in_ready_queue.resource1_usage <= self.reamining_resource1_number and first_task_in_ready_queue.resource2_usage <= self.reamining_resource2_number:
                                        self.reamining_resource1_number -= first_task_in_ready_queue.resource1_usage
                                        self.reamining_resource2_number -= first_task_in_ready_queue.resource2_usage
                                        pickuped_task = first_task_in_ready_queue
                                        is_pick_task = True
                                        self.processor1_is_ok = True
                                    else:
                                        with self.waiting_queue_lock:
                                            self.Waiting_queue.put((first_task_in_ready_queue.get_remaining_execution_time(), first_task_in_ready_queue))
                                            print(f"SUBSYSTEM 1 : THIS TASK {first_task_in_ready_queue} MOVED TO WAITING QUEUE BECAUSE THERE IS NO AVAILABLE RESOURCES NOW.")
                                        is_pick_task = False  
                                        self.processor1_is_ok = False     
                        else: 
                            '''
                            Ready Queue is Empty at first
                            '''
                            print("SUBSYSTEM 1 : Ready Queue1 is Empty and Request for Task (Ready Queue is Empty at first)")
                            self.subsystem_did['processor1'] = "IDLE"  
                            self.request_task(1)
                            is_pick_task = False
                            empty_at_first = True
                    
                    if is_pick_task:
                        self.processor1_assigned_task = pickuped_task
                        with self.ready_queue_lock:
                            self.processor1_busy_time = weighted_round_robbin(self.Ready_queue1, self.processor1_assigned_task)
                        # EXECUTION
                        self.processor1_assigned_task.assigned_quantum = self.processor1_busy_time
                        print(f"SUBSYSTEM 1 : THIS TASK GET PROCESSOR 1 => {self.processor1_assigned_task}, AND GET QUANTUM = {self.processor1_assigned_task.assigned_quantum}, AND THIS RESOURCES : R1 = {self.processor1_assigned_task.resource1_usage}, R2 = {self.processor1_assigned_task.resource2_usage}")
                        self.subsystem_did['processor1'] = self.processor1_assigned_task
                        self.processor1_assigned_task.proceed_executed_time += 1
                        self.processor1_busy_time -= 1
                        remaining_time = self.processor1_assigned_task.get_remaining_execution_time()
                        if remaining_time <= 0:
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor1_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor1_assigned_task.resource2_usage
                            print(f"SUBSYSTEM 1 : THIS TASK FINISED IN PROCESSOR 1 => {self.processor1_assigned_task} AND GIVE BACK THIS RESOURCES R1 = {self.processor1_assigned_task.resource1_usage}, R2 = {self.processor1_assigned_task.resource2_usage}")
                            self.finished_tasks.append(self.processor1_assigned_task)
                            self.processor1_assigned_task = None
                            self.processor1_busy_time = 0
                        if remaining_time > 0 and self.processor1_busy_time <= 0:
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor1_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor1_assigned_task.resource2_usage
                            print(f"SUBSYSTEM 1 : ENDED QUANTUM OF THIS TASK IN PROCESSOR 1 => {self.processor1_assigned_task} AND GIVE BACK THIS RESOURCES R1 = {self.processor1_assigned_task.resource1_usage}, R2 = {self.processor1_assigned_task.resource2_usage}")
                            with self.ready_queue_lock:
                                self.Ready_queue1.append(self.processor1_assigned_task)
                                
                            self.processor1_assigned_task = None
                            self.processor1_busy_time = 0
                    elif not is_pick_task and not empty_at_first: 
                        '''
                        there Was a task in ready queue 
                        but cant assign any of them to cpu
                        and sent all those task to waiting queue
                        '''
                        self.subsystem_did['processor1'] = "IDLE" 
                        print('''SUBSYSTEM 1 : Ready Queue1 is Empty and Request for Task''')
                        self.request_task(1)
                         
                self.processor1_status = False
                        

    def processor2(self):
        while True:
            if self.processor2_status:
                
                if self.processor2_busy_time > 0: # there is a task that should be run
                    if self.processor2_assigned_task:
                        # EXECUTION
                        self.subsystem_did['processor2'] = self.processor2_assigned_task
                        self.processor2_assigned_task.proceed_executed_time += 1 
                        self.processor2_busy_time -= 1
                        remaining_time = self.processor2_assigned_task.get_remaining_execution_time()
                        if remaining_time <= 0:
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor2_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor2_assigned_task.resource2_usage
                            print(f"SUBSYSTEM 1 : THIS TASK FINISED IN PROCESSOR 2 => {self.processor2_assigned_task} AND GIVE BACK THIS RESOURCES R1 = {self.processor2_assigned_task.resource1_usage}, R2 = {self.processor2_assigned_task.resource2_usage}")
                            self.finished_tasks.append(self.processor2_assigned_task)
                            self.processor2_assigned_task = None
                            self.processor2_busy_time = 0
                        if remaining_time > 0 and self.processor2_busy_time <= 0: # preempt task from processor
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor2_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor2_assigned_task.resource2_usage
                            print(f"SUBSYSTEM 1 : ENDED QUANTUM OF THIS TASK IN PROCESSOR 2 => {self.processor2_assigned_task} AND GIVE BACK THIS RESOURCES R1 = {self.processor2_assigned_task.resource1_usage}, R2 = {self.processor2_assigned_task.resource2_usage}")
                            with self.ready_queue_lock:
                                self.Ready_queue2.append(self.processor2_assigned_task)
                               
                            self.processor2_assigned_task = None
                            self.processor2_busy_time = 0
                            
                elif self.processor2_busy_time <= 0:
                    
                    empty_at_first = False
                    is_pick_task = False
                    pickuped_task = None    
                    with self.ready_queue_lock:
                        if len(self.Ready_queue2) > 0:
                            while len(self.Ready_queue2) > 0 and not is_pick_task: # try to assign task
                                first_task_in_ready_queue = self.Ready_queue2.pop(0)
                                with self.resource_lock:
                                    if first_task_in_ready_queue.resource1_usage <= self.reamining_resource1_number and first_task_in_ready_queue.resource2_usage <= self.reamining_resource2_number:
                                        self.reamining_resource1_number -= first_task_in_ready_queue.resource1_usage
                                        self.reamining_resource2_number -= first_task_in_ready_queue.resource2_usage
                                        pickuped_task = first_task_in_ready_queue
                                        is_pick_task = True
                                        self.processor2_is_ok = True
                                    else:
                                        with self.waiting_queue_lock:
                                            self.Waiting_queue.put((first_task_in_ready_queue.get_remaining_execution_time(), first_task_in_ready_queue))
                                            print(f"SUBSYSTEM 1 : THIS TASK {first_task_in_ready_queue} MOVED TO WAITING QUEUE BECAUSE THERE IS NO AVAILABLE RESOURCES NOW.")
                                        is_pick_task = False  
                                        self.processor2_is_ok = False     
                        else: 
                            '''
                            Ready Queue is Empty at first
                            '''
                            print("SUBSYSTEM 1 : Ready Queue2 is Empty and Request for Task (Ready Queue is Empty at first)")
                            self.subsystem_did['processor2'] = 'IDLE'
                            self.request_task(2)
                            is_pick_task = False
                            empty_at_first = True
                    
                    if is_pick_task:
                        self.processor2_assigned_task = pickuped_task
                        with self.ready_queue_lock:
                            self.processor2_busy_time = weighted_round_robbin(self.Ready_queue2, self.processor2_assigned_task)
                        # EXECUTION
                        self.processor2_assigned_task.assigned_quantum = self.processor2_busy_time
                        print(f"SUBSYSTEM 1 : THIS TASK GET PROCESSOR 2 => {self.processor2_assigned_task}, AND GET QUANTUM = {self.processor2_assigned_task.assigned_quantum}, AND THIS RESOURCES : R1 = {self.processor2_assigned_task.resource1_usage}, R2 = {self.processor2_assigned_task.resource2_usage}")
                        self.subsystem_did['processor2'] = self.processor2_assigned_task
                        self.processor2_assigned_task.proceed_executed_time += 1
                        self.processor2_busy_time -= 1
                        remaining_time = self.processor2_assigned_task.get_remaining_execution_time()
                        if remaining_time <= 0:
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor2_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor2_assigned_task.resource2_usage
                            print(f"SUBSYSTEM 1 : THIS TASK FINISED IN PROCESSOR 2 => {self.processor2_assigned_task} AND GIVE BACK THIS RESOURCES R1 = {self.processor2_assigned_task.resource1_usage}, R2 = {self.processor2_assigned_task.resource2_usage}")
                            self.finished_tasks.append(self.processor2_assigned_task)
                            self.processor2_assigned_task = None
                            self.processor2_busy_time = 0
                        if remaining_time > 0 and self.processor2_busy_time <= 0:
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor2_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor2_assigned_task.resource2_usage
                            print(f"SUBSYSTEM 1 : ENDED QUANTUM OF THIS TASK IN PROCESSOR 2 => {self.processor2_assigned_task} AND GIVE BACK THIS RESOURCES R1 = {self.processor2_assigned_task.resource1_usage}, R2 = {self.processor2_assigned_task.resource2_usage}")
                            with self.ready_queue_lock:
                                self.Ready_queue2.append(self.processor2_assigned_task)                                
                                
                            self.processor2_assigned_task = None
                            self.processor2_busy_time = 0
                    elif not is_pick_task and not empty_at_first: 
                        '''
                        there Was a task in ready queue 
                        but cant assign any of them to cpu
                        and sent all those task to waiting queue
                        '''
                        self.subsystem_did['processor2'] = "IDLE"
                        print('''SUBSYSTEM 1 : Ready Queue2 is Empty and Request for Task''')
                        self.request_task(2)
                         
                self.processor2_status = False
    
    def processor3(self):
        while True:
            if self.processor3_status:
                
                if self.processor3_busy_time > 0: # there is a task that should be run
                    if self.processor3_assigned_task:
                        # EXECUTION
                        self.subsystem_did['processor3'] = self.processor3_assigned_task
                        self.processor3_assigned_task.proceed_executed_time += 1 
                        self.processor3_busy_time -= 1
                        remaining_time = self.processor3_assigned_task.get_remaining_execution_time()
                        if remaining_time <= 0:
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor3_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor3_assigned_task.resource2_usage
                            print(f"SUBSYSTEM 1 : THIS TASK FINISED IN PROCESSOR 3 => {self.processor3_assigned_task} AND GIVE BACK THIS RESOURCES R1 = {self.processor3_assigned_task.resource1_usage}, R2 = {self.processor3_assigned_task.resource2_usage}")
                            self.finished_tasks.append(self.processor3_assigned_task)
                            self.processor3_assigned_task = None
                            self.processor3_busy_time = 0
                        if remaining_time > 0 and self.processor3_busy_time <= 0: # preempt task from processor
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor3_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor3_assigned_task.resource2_usage
                            print(f"SUBSYSTEM 1 : ENDED QUANTUM OF THIS TASK IN PROCESSOR 3 => {self.processor3_assigned_task} AND GIVE BACK THIS RESOURCES R1 = {self.processor3_assigned_task.resource1_usage}, R2 = {self.processor3_assigned_task.resource2_usage}")
                            with self.ready_queue_lock:
                                self.Ready_queue3.append(self.processor3_assigned_task)
                                
                            self.processor3_assigned_task = None
                            self.processor3_busy_time = 0
                            
                elif self.processor3_busy_time <= 0:
                    
                    empty_at_first = False
                    is_pick_task = False
                    pickuped_task = None    
                    with self.ready_queue_lock:
                        if len(self.Ready_queue3) > 0:
                            while len(self.Ready_queue3) > 0 and not is_pick_task: # try to assign task
                                first_task_in_ready_queue = self.Ready_queue3.pop(0)
                                with self.resource_lock:
                                    if first_task_in_ready_queue.resource1_usage <= self.reamining_resource1_number and first_task_in_ready_queue.resource2_usage <= self.reamining_resource2_number:
                                        self.reamining_resource1_number -= first_task_in_ready_queue.resource1_usage
                                        self.reamining_resource2_number -= first_task_in_ready_queue.resource2_usage
                                        pickuped_task = first_task_in_ready_queue
                                        is_pick_task = True
                                    else:
                                        with self.waiting_queue_lock:
                                            self.Waiting_queue.put((first_task_in_ready_queue.get_remaining_execution_time(), first_task_in_ready_queue))
                                            print(f"SUBSYSTEM 1 : THIS TASK {first_task_in_ready_queue} MOVED TO WAITING QUEUE BECAUSE THERE IS NO AVAILABLE RESOURCES NOW.")
                                        is_pick_task = False  
                        else: 
                            '''
                            Ready Queue is Empty at first
                            '''
                            self.subsystem_did['processor3'] ="IDLE"
                            print("SUBSYSTEM 1 : Ready Queue3 is Empty and Request for Task (Ready Queue is Empty at first)")
                            self.request_task(3)
                            is_pick_task = False
                            empty_at_first = True
                    
                    if is_pick_task:
                        self.processor3_assigned_task = pickuped_task
                        with self.ready_queue_lock:
                            self.processor3_busy_time = weighted_round_robbin(self.Ready_queue3, self.processor3_assigned_task)
                        # EXECUTION
                        self.processor3_assigned_task.assigned_quantum = self.processor3_busy_time
                        print(f"SUBSYSTEM 1 : THIS TASK GET PROCESSOR 3 => {self.processor3_assigned_task}, AND GET QUANTUM = {self.processor3_assigned_task.assigned_quantum}, AND THIS RESOURCES : R1 = {self.processor3_assigned_task.resource1_usage}, R2 = {self.processor3_assigned_task.resource2_usage}")
                        self.subsystem_did['processor3'] = self.processor3_assigned_task
                        self.processor3_assigned_task.proceed_executed_time += 1
                        self.processor3_busy_time -= 1
                        remaining_time = self.processor3_assigned_task.get_remaining_execution_time()
                        if remaining_time <= 0:
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor3_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor3_assigned_task.resource2_usage
                            print(f"SUBSYSTEM 1 : THIS TASK FINISED IN PROCESSOR 3 => {self.processor3_assigned_task} AND GIVE BACK THIS RESOURCES R1 = {self.processor3_assigned_task.resource1_usage}, R2 = {self.processor3_assigned_task.resource2_usage}")
                            self.finished_tasks.append(self.processor3_assigned_task)
                            self.processor3_assigned_task = None
                            self.processor3_busy_time = 0
                        if remaining_time > 0 and self.processor3_busy_time <= 0:
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor3_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor3_assigned_task.resource2_usage
                            print(f"SUBSYSTEM 1 : ENDED QUANTUM OF THIS TASK IN PROCESSOR 3 => {self.processor3_assigned_task} AND GIVE BACK THIS RESOURCES R1 = {self.processor3_assigned_task.resource1_usage}, R2 = {self.processor3_assigned_task.resource2_usage}")
                            with self.ready_queue_lock:
                                self.Ready_queue3.append(self.processor3_assigned_task)
                                
                            self.processor3_assigned_task = None
                            self.processor3_busy_time = 0
                    elif not is_pick_task and not empty_at_first: 
                        '''
                        there Was a task in ready queue 
                        but cant assign any of them to cpu
                        and sent all those task to waiting queue
                        '''
                        self.subsystem_did['processor3'] = "IDLE"
                        print('''SUBSYSTEM 1 : Ready Queue3 is Empty and Request for Task''')
                        self.request_task(3)
                         
                self.processor3_status = False

    def start_subsystem(self):
        processor1_thread = threading.Thread(target=self.processor1)
        processor2_thread = threading.Thread(target=self.processor2)
        processor3_thread = threading.Thread(target =self.processor3)

        processor1_thread.start()
        processor2_thread.start()
        processor3_thread.start()

        # Don't join here - let the thread run independently
        return

