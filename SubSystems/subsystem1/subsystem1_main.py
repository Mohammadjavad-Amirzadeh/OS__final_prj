import time
import queue 
import threading
from SubSystems.subsystem1.subsystem1_task import subsystem1_task
from Resources.Resource1 import resource1
from Resources.Resource2 import resource2



class subsystem1:
    def __init__(self, subsystem1_tasks, resource1_number, resource2_number):
        self.subsystem_number = 1
        self.processors_count = 3
        self.tasks = subsystem1_tasks
        self.Waiting_queue = queue.PriorityQueue()
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
        self.add_to_waiting_queue()
        
        self.processor1_status = False
        self.processor2_status = False
        self.processor3_status = False
        
        self.processor1_busy_time = 0
        self.processor2_busy_time = 0
        self.processor3_busy_time = 0
        
        self.processor1_assigned_task = None
        self.processor2_assigned_task = None
        self.processor3_assigned_task = None
        
        self.finished_tasks = []
        
        self.subsystem1_clock = threading.Event()
        self.resource_lock = threading.Lock()
        self.waiting_queue_lock = threading.Lock()
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
        
    def add_to_waiting_queue(self):
        for task in self.tasks:
            self.Waiting_queue.put((task.arrival_time, task))
    
    def move_all_tasks_to_ready_queue(self):
        while not self.Waiting_queue.empty():
            task = self.Waiting_queue.get()[1]
            # self.Waiting_queue.put((task.arrival_time, task))
            if task.processor_number == 1:
                self.Ready_queue1.append(task)
            elif task.processor_number == 2:
                self.Ready_queue2.append(task)
            elif task.processor_number == 3:
                self.Ready_queue3.append(task)
            else:
                raise("WRONG PROCESSOR NUMBER DETECTED")
            task.state = 'Ready'

        
    def print_waiting_queue(self):
        print("Waiting Queue:", self.Waiting_queue.qsize())
        for _, task in list(self.Waiting_queue.queue):
            print(f"Task {task.name}, Arrival Time: {task.arrival_time}, State: {task.state}")
            
    def print_ready_queue1(self):
        print("Ready Queue 1 :")
        for task in self.Ready_queue1:
            print(f"Task {task.name}, Arrival Time: {task.arrival_time}, State: {task.state}")
    
    def print_ready_queue2(self):
        print("Ready Queue 2 :")
        for task in self.Ready_queue2:
            print(f"Task {task.name}, Arrival Time: {task.arrival_time}, State: {task.state}")
            
    def print_ready_queue3(self):
        print("Ready Queue 3 :")
        for task in self.Ready_queue3:
            print(f"Task {task.name}, Arrival Time: {task.arrival_time}, State: {task.state}")
            
    def set_clock(self):
        self.current_time += 1  # Add this line to increment time
        self.processor1_status = True
        self.processor2_status = True
        self.processor3_status = True
        
    def is_processores_finished(self):
        return not(self.processor1_status) and not(self.processor2_status) and not(self.processor3_status)
    
    def processor1(self):
        while True:
            if self.processor1_status:
                if self.processor1_busy_time > 0:
                    if self.processor1_assigned_task:
                        self.processor1_assigned_task.proceed_executed_time += 1
                        self.processor1_busy_time -= 1
                        remaining_time = self.processor1_assigned_task.get_remaining_execution_time()
                        if remaining_time <= 0:  # task ended quantum > remaining execution time
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor1_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor1_assigned_task.resource2_usage

                            self.finished_tasks.append(self.processor1_assigned_task)
                            self.processor1_assigned_task = None
                            self.processor1_busy_time = 0
                        elif self.processor1_busy_time <= 0 and remaining_time > 0:  # task not end but exceeded given quantum
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor1_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor1_assigned_task.resource2_usage
                            self.Ready_queue1.append(self.processor1_assigned_task)
                            self.processor1_assigned_task = None
                            self.processor1_busy_time = 0

                elif self.processor1_busy_time <= 0:    
                    time.sleep(0.1)
                    task = None
                    flag = False
                    has_ready_tasks = False
                    
                    # First check if any tasks are ready now
                    for task in self.Ready_queue1:
                        if task.arrival_time <= self.current_time:
                            has_ready_tasks = True
                            break
                    
                    # Only try to process if we have ready tasks
                    if has_ready_tasks and len(self.Ready_queue1) > 0:
                        while len(self.Ready_queue1) > 0:
                            task = self.Ready_queue1.pop(0)
                            
                            if task.arrival_time > self.current_time:
                                self.Ready_queue1.append(task)
                                continue
                            
                            with self.resource_lock:
                                if task.resource1_usage <= self.reamining_resource1_number and task.resource2_usage <= self.reamining_resource2_number:
                                    self.reamining_resource1_number -= task.resource1_usage
                                    self.reamining_resource2_number -= task.resource2_usage
                                    flag = True
                                    break
                                else:
                                    self.Waiting_queue.put((task.get_remaining_execution_time(), task))
                        
                        if flag:
                            self.processor1_assigned_task = task
                            self.processor1_busy_time = 2
                            # Process first tick immediately
                            self.processor1_assigned_task.proceed_executed_time += 1
                            self.processor1_busy_time -= 1
                            remaining_time = self.processor1_assigned_task.get_remaining_execution_time()
                            if remaining_time <= 0:
                                with self.resource_lock:
                                    self.reamining_resource1_number += self.processor1_assigned_task.resource1_usage
                                    self.reamining_resource2_number += self.processor1_assigned_task.resource2_usage

                                self.finished_tasks.append(self.processor1_assigned_task)
                                self.processor1_assigned_task = None
                                self.processor1_busy_time = 0
                            elif self.processor1_busy_time <= 0 and remaining_time > 0:
                                with self.resource_lock:
                                    self.reamining_resource1_number += self.processor1_assigned_task.resource1_usage
                                    self.reamining_resource2_number += self.processor1_assigned_task.resource2_usage
                                self.Ready_queue1.append(self.processor1_assigned_task)
                                self.processor1_assigned_task = None
                                self.processor1_busy_time = 0
                    else:
                        print("No ready tasks for processor 1")
                        
                self.processor1_status = False

    def processor2(self):
        while True:
            if self.processor2_status:
                if self.processor2_busy_time > 0:
                    if self.processor2_assigned_task:
                        self.processor2_assigned_task.proceed_executed_time += 1
                        self.processor2_busy_time -= 1
                        remaining_time = self.processor2_assigned_task.get_remaining_execution_time()
                        if remaining_time <= 0: # task ended quantum > remaining execution time
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor2_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor2_assigned_task.resource2_usage

                            self.finished_tasks.append(self.processor2_assigned_task)
                            self.processor2_assigned_task = None
                            self.processor2_busy_time = 0
                        elif self.processor2_busy_time <= 0 and remaining_time > 0: # task not end but exceeded given quantum
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor2_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor2_assigned_task.resource2_usage
                            self.Ready_queue2.append(self.processor2_assigned_task)
                            self.processor2_assigned_task = None
                            self.processor2_busy_time = 0
                elif self.processor2_busy_time <= 0:    
                    time.sleep(0.1)
                    task = None
                    flag = False
                    has_ready_tasks = False
                    
                    # First check if any tasks are ready now
                    for task in self.Ready_queue2:
                        if task.arrival_time <= self.current_time:
                            has_ready_tasks = True
                            break
                    
                    # Only try to process if we have ready tasks
                    if has_ready_tasks and len(self.Ready_queue2) > 0:
                        while len(self.Ready_queue2) > 0:
                            task = self.Ready_queue2.pop(0)
                            
                            if task.arrival_time > self.current_time:
                                self.Ready_queue2.append(task)
                                continue
                            
                            with self.resource_lock:
                                if task.resource1_usage <= self.reamining_resource1_number and task.resource2_usage <= self.reamining_resource2_number:
                                    self.reamining_resource1_number -= task.resource1_usage
                                    self.reamining_resource2_number -= task.resource2_usage
                                    flag = True
                                    break
                                else:
                                    self.Waiting_queue.put((task.get_remaining_execution_time(), task))
                        
                        if flag:
                            self.processor2_assigned_task = task
                            self.processor2_busy_time = 2
                            # Process first tick immediately
                            self.processor2_assigned_task.proceed_executed_time += 1
                            self.processor2_busy_time -= 1
                            remaining_time = self.processor2_assigned_task.get_remaining_execution_time()
                            if remaining_time <= 0:
                                with self.resource_lock:
                                    self.reamining_resource1_number += self.processor2_assigned_task.resource1_usage
                                    self.reamining_resource2_number += self.processor2_assigned_task.resource2_usage

                                self.finished_tasks.append(self.processor2_assigned_task)
                                self.processor2_assigned_task = None
                                self.processor2_busy_time = 0
                            elif self.processor2_busy_time <= 0 and remaining_time > 0:
                                with self.resource_lock:
                                    self.reamining_resource1_number += self.processor2_assigned_task.resource1_usage
                                    self.reamining_resource2_number += self.processor2_assigned_task.resource2_usage
                                self.Ready_queue2.append(self.processor2_assigned_task)
                                self.processor2_assigned_task = None
                                self.processor2_busy_time = 0
                    else:
                        print("No ready tasks for processor 2")
                        
                self.processor2_status = False
    
    def processor3(self):
        while True:
            if self.processor3_status:
                if self.processor3_busy_time > 0:
                    if self.processor3_assigned_task:
                        self.processor3_assigned_task.proceed_executed_time += 1
                        self.processor3_busy_time -= 1
                        remaining_time = self.processor3_assigned_task.get_remaining_execution_time()
                        if remaining_time <= 0:  # task ended quantum > remaining execution time
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor3_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor3_assigned_task.resource2_usage

                            self.finished_tasks.append(self.processor3_assigned_task)
                            self.processor3_assigned_task = None
                            self.processor3_busy_time = 0
                        elif self.processor3_busy_time <= 0 and remaining_time > 0:  # task not end but exceeded given quantum
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor3_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor3_assigned_task.resource2_usage
                            self.Ready_queue3.append(self.processor3_assigned_task)
                            self.processor3_assigned_task = None
                            self.processor3_busy_time = 0
                elif self.processor3_busy_time <= 0:    
                    time.sleep(0.1)
                    task = None
                    flag = False
                    has_ready_tasks = False
                    
                    # First check if any tasks are ready now
                    for task in self.Ready_queue3:
                        if task.arrival_time <= self.current_time:
                            has_ready_tasks = True
                            break
                    
                    # Only try to process if we have ready tasks
                    if has_ready_tasks and len(self.Ready_queue3) > 0:
                        while len(self.Ready_queue3) > 0:
                            task = self.Ready_queue3.pop(0)
                            
                            if task.arrival_time > self.current_time:
                                self.Ready_queue3.append(task)
                                continue
                            
                            with self.resource_lock:
                                if task.resource1_usage <= self.reamining_resource1_number and task.resource2_usage <= self.reamining_resource2_number:
                                    self.reamining_resource1_number -= task.resource1_usage
                                    self.reamining_resource2_number -= task.resource2_usage
                                    flag = True
                                    break
                                else:
                                    self.Waiting_queue.put((task.get_remaining_execution_time(), task))
                        
                        if flag:
                            self.processor3_assigned_task = task
                            self.processor3_busy_time = 2
                            # Process first tick immediately
                            self.processor3_assigned_task.proceed_executed_time += 1
                            self.processor3_busy_time -= 1
                            remaining_time = self.processor3_assigned_task.get_remaining_execution_time()
                            if remaining_time <= 0:
                                with self.resource_lock:
                                    self.reamining_resource1_number += self.processor3_assigned_task.resource1_usage
                                    self.reamining_resource2_number += self.processor3_assigned_task.resource2_usage

                                self.finished_tasks.append(self.processor3_assigned_task)
                                self.processor3_assigned_task = None
                                self.processor3_busy_time = 0
                            elif self.processor3_busy_time <= 0 and remaining_time > 0:
                                with self.resource_lock:
                                    self.reamining_resource1_number += self.processor3_assigned_task.resource1_usage
                                    self.reamining_resource2_number += self.processor3_assigned_task.resource2_usage
                                self.Ready_queue3.append(self.processor3_assigned_task)
                                self.processor3_assigned_task = None
                                self.processor3_busy_time = 0
                    else:
                        print("No ready tasks for processor 3")
                        
                self.processor3_status = False

    def start_subsystem(self):
        self.move_all_tasks_to_ready_queue()
        processor1_thread = threading.Thread(target=self.processor1)
        processor2_thread = threading.Thread(target=self.processor2)
        processor3_thread = threading.Thread(target =self.processor3)

        processor1_thread.start()
        processor2_thread.start()
        processor3_thread.start()

        # Don't join here - let the thread run independently
        return

