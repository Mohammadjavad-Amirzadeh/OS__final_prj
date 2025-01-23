import queue 
import threading

class subsystem2:
    def __init__(self, subsystem2_tasks, resource1_number, resource2_number):
        self.processors_count = 2
        self.tasks = subsystem2_tasks
        self.Ready_queue = queue.PriorityQueue()
        self.resource1_number = resource1_number
        self.resource2_number = resource2_number
        self.reamining_resource1_number = resource1_number
        self.reamining_resource2_number = resource2_number
        self.resource1_list = []
        self.resource2_list = []
        self.initiate_resources()
        
        self.storing_all_tasks = queue.PriorityQueue()
        
        self.processor1_status = False
        self.processor2_status = False
        
        self.processor1_busy_time = 0
        self.processor2_busy_time = 0
        
        self.processor1_assigned_task = None
        self.processor2_assigned_task = None
        
        self.finished_and_aborted_tasks = []
        
        
        self.resource_lock = threading.Lock()
        self.ready_queue_lock = threading.Lock()
        
        self.current_time = -1
        
        
        
    def initiate_resources(self):
        for resource in range(self.resource1_number):
            self.resource1_list.append(resource1(self.subsystem_number))
        for resource in range(self.resource2_number):
            self.resource1_list.append(resource1(self.subsystem_number))
            
    def set_clock(self):
        self.current_time += 1  # Add this line to increment time
        self.processor1_status = True
        self.processor2_status = True
        self.processor3_status = True
        self.check_add_task_by_arrival_time()
        
    def is_processores_finished(self):
        return not(self.processor1_status) and not(self.processor2_status) and not(self.processor3_status)
        
    def check_add_task_by_arrival_time(self):
        while not self.storing_all_tasks.empty():
            priority, task = self.storing_all_tasks.get()
            if task.arrival_time <= self.current_time:
                self.Ready_queue.put((priority, task))
            else:
                self.storing_all_tasks.put((priority, task))
        
    def move_all_tasks_to_temp_list(self):
        for task in self.tasks:
            self.storing_all_tasks.put((task.arrival_time, task))
            
    def check_safety(self, task):
        return task.resource1_usage > self.resource1_number and task.resource2_usage > self.resource2_number
        
    def processor1(self):
        while True:
            if self.processor1_status:
                if self.processor1_busy_time > 0:
                    if self.processor1_assigned_task:
                        # check if a new task should run or not 
                        is_pick_task = False
                        pickuped_task = None
                        while not self.Ready_queue.empty():
                            priority_of_shortest_task_in_ready_queue, shortest_task_in_ready_queue = None, None
                            with self.ready_queue_lock:
                                priority_of_shortest_task_in_ready_queue, shortest_task_in_ready_queue = self.Ready_queue.get()
                            if shortest_task_in_ready_queue.get_remaining_execution_time() < self.processor1_assigned_task.get_remaining_execution_time(): # there is a shorter processor in ready queue
                                if self.check_safety(shortest_task_in_ready_queue):
                                    pickuped_task = shortest_task_in_ready_queue
                                    is_pick_task = True
                                else:
                                    self.finished_and_aborted_tasks.append(shortest_task_in_ready_queue)
                                    
                            else:
                                is_pick_task = False
                                self.Ready_queue.put((priority_of_shortest_task_in_ready_queue, shortest_task_in_ready_queue))

                                
                        # if a new task choosed and should run
                        if is_pick_task: 
                            with self.ready_queue_lock:
                                self.Ready_queue.put((self.processor1_assigned_task.get_remaining_execution_time(), self.processor1_assigned_task))
                            self.processor1_assigned_task = pickuped_task
                            self.processor1_busy_time = self.processor1_assigned_task.get_remaining_execution_time()
                            is_ok = False
                            while not is_ok:
                                with self.ready_queue_lock:
                                    if self.reamining_resource1_number > self.processor1_assigned_task.resource1_usage and self.reamining_resource2_number > self.processor1_assigned_task.resource2_usage:
                                        self.reamining_resource1_number -= self.processor1_assigned_task.resource1_usage
                                        self.reamining_resource2_number -= self.processor1_assigned_task.resource2_usage
                                        is_ok = True
                            self.processor1_assigned_task.proceed_executed_time += 1
                            self.processor1_busy_time -= 1
                            remaining_time = self.processor1_assigned_task.get_remaining_execution_time()
                            if remaining_time <= 0: # task ended
                                with self.resource_lock:
                                    self.reamining_resource1_number += self.processor1_assigned_task.resource1_usage
                                    self.reamining_resource2_number += self.processor1_assigned_task.resource2_usage
                                self.finished_and_aborted_tasks.append(self.processor1_assigned_task)
                                self.processor1_assigned_task = None
                                self.processor1_busy_time = 0 
                                
                        # previous task should execute its run  
                        else:
                            self.processor1_assigned_task.proceed_executed_time += 1
                            self.processor1_busy_time -= 1
                            remaining_time = self.processor1_assigned_task.get_remaining_execution_time()
                            if remaining_time <= 0: # task ended
                                with self.resource_lock:
                                    self.reamining_resource1_number += self.processor1_assigned_task.resource1_usage
                                    self.reamining_resource2_number += self.processor1_assigned_task.resource2_usage
                                self.finished_and_aborted_tasks.append(self.processor1_assigned_task)
                                self.processor1_assigned_task = None
                                self.processor1_busy_time = 0   

                elif self.processor1_busy_time <= 0:   
                    is_pick_task = False
                    pickuped_task = None
                    while not self.Ready_queue.empty():
                        priority_of_shortest_task_in_ready_queue, shortest_task_in_ready_queue = None, None
                        with self.ready_queue_lock:
                            priority_of_shortest_task_in_ready_queue, shortest_task_in_ready_queue = self.Ready_queue.get()
                        if shortest_task_in_ready_queue.get_remaining_execution_time() < self.processor1_assigned_task.get_remaining_execution_time(): # there is a shorter processor in ready queue
                            if self.check_safety(shortest_task_in_ready_queue):
                                pickuped_task = shortest_task_in_ready_queue
                                is_pick_task = True
                            else:
                                self.finished_and_aborted_tasks.append(shortest_task_in_ready_queue)
                        else:
                            is_pick_task = False
                            self.Ready_queue.put((priority_of_shortest_task_in_ready_queue, shortest_task_in_ready_queue))

                            
                    if pickuped_task and is_pick_task:
                        with self.ready_queue_lock:
                            self.Ready_queue.put((self.processor1_assigned_task.get_remaining_execution_time(), self.processor1_assigned_task))
                        self.processor1_assigned_task = pickuped_task
                        self.processor1_busy_time = self.processor1_assigned_task.get_remaining_execution_time()
                        is_ok = False
                        while not is_ok:
                            with self.ready_queue_lock:
                                if self.reamining_resource1_number > self.processor1_assigned_task.resource1_usage and self.reamining_resource2_number > self.processor1_assigned_task.resource2_usage:
                                    self.reamining_resource1_number -= self.processor1_assigned_task.resource1_usage
                                    self.reamining_resource2_number -= self.processor1_assigned_task.resource2_usage
                                    is_ok = True
                        self.processor1_assigned_task.proceed_executed_time += 1
                        self.processor1_busy_time -= 1
                        remaining_time = self.processor1_assigned_task.get_remaining_execution_time()
                        if remaining_time <= 0: # task ended
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor1_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor1_assigned_task.resource2_usage
                            self.finished_and_aborted_tasks.append(self.processor1_assigned_task)
                            self.processor1_assigned_task = None
                            self.processor1_busy_time = 0 
                    else:
                        print("Cant Pickup a Task")
                        
                self.processor1_status = False

    
    def processor2(self):
        while True:
            if self.processor2_status:
                if self.processor2_busy_time > 0:
                    if self.processor2_assigned_task:
                        # check if a new task should run or not 
                        is_pick_task = False
                        pickuped_task = None
                        while not self.Ready_queue.empty():
                            priority_of_shortest_task_in_ready_queue, shortest_task_in_ready_queue = None, None
                            with self.ready_queue_lock:
                                priority_of_shortest_task_in_ready_queue, shortest_task_in_ready_queue = self.Ready_queue.get()
                            if shortest_task_in_ready_queue.get_remaining_execution_time() < self.processor2_assigned_task.get_remaining_execution_time(): # there is a shorter processor in ready queue
                                if self.check_safety(shortest_task_in_ready_queue):
                                    pickuped_task = shortest_task_in_ready_queue
                                    is_pick_task = True
                                else:
                                    self.finished_and_aborted_tasks.append(shortest_task_in_ready_queue)
                                    
                            else:
                                is_pick_task = False
                                self.Ready_queue.put((priority_of_shortest_task_in_ready_queue, shortest_task_in_ready_queue))

                                
                        # if a new task choosed and should run
                        if is_pick_task: 
                            with self.ready_queue_lock:
                                self.Ready_queue.put((self.processor2_assigned_task.get_remaining_execution_time(), self.processor2_assigned_task))
                            self.processor2_assigned_task = pickuped_task
                            self.processor2_busy_time = self.processor2_assigned_task.get_remaining_execution_time()
                            is_ok = False
                            while not is_ok:
                                with self.ready_queue_lock:
                                    if self.reamining_resource1_number > self.processor2_assigned_task.resource1_usage and self.reamining_resource2_number > self.processor2_assigned_task.resource2_usage:
                                        self.reamining_resource1_number -= self.processor2_assigned_task.resource1_usage
                                        self.reamining_resource2_number -= self.processor2_assigned_task.resource2_usage
                                        is_ok = True
                            self.processor2_assigned_task.proceed_executed_time += 1
                            self.processor2_busy_time -= 1
                            remaining_time = self.processor2_assigned_task.get_remaining_execution_time()
                            if remaining_time <= 0: # task ended
                                with self.resource_lock:
                                    self.reamining_resource1_number += self.processor2_assigned_task.resource1_usage
                                    self.reamining_resource2_number += self.processor2_assigned_task.resource2_usage
                                self.finished_and_aborted_tasks.append(self.processor2_assigned_task)
                                self.processor2_assigned_task = None
                                self.processor2_busy_time = 0 
                                
                        # previous task should execute its run  
                        else:
                            self.processor2_assigned_task.proceed_executed_time += 1
                            self.processor2_busy_time -= 1
                            remaining_time = self.processor2_assigned_task.get_remaining_execution_time()
                            if remaining_time <= 0: # task ended
                                with self.resource_lock:
                                    self.reamining_resource1_number += self.processor2_assigned_task.resource1_usage
                                    self.reamining_resource2_number += self.processor2_assigned_task.resource2_usage
                                self.finished_and_aborted_tasks.append(self.processor2_assigned_task)
                                self.processor2_assigned_task = None
                                self.processor2_busy_time = 0   

                elif self.processor2_busy_time <= 0:   
                    is_pick_task = False
                    pickuped_task = None
                    while not self.Ready_queue.empty():
                        priority_of_shortest_task_in_ready_queue, shortest_task_in_ready_queue = None, None
                        with self.ready_queue_lock:
                            priority_of_shortest_task_in_ready_queue, shortest_task_in_ready_queue = self.Ready_queue.get()
                        if shortest_task_in_ready_queue.get_remaining_execution_time() < self.processor2_assigned_task.get_remaining_execution_time(): # there is a shorter processor in ready queue
                            if self.check_safety(shortest_task_in_ready_queue):
                                pickuped_task = shortest_task_in_ready_queue
                                is_pick_task = True
                            else:
                                self.finished_and_aborted_tasks.append(shortest_task_in_ready_queue)
                        else:
                            is_pick_task = False
                            self.Ready_queue.put((priority_of_shortest_task_in_ready_queue, shortest_task_in_ready_queue))

                            
                    if pickuped_task and is_pick_task:
                        with self.ready_queue_lock:
                            self.Ready_queue.put((self.processor2_assigned_task.get_remaining_execution_time(), self.processor2_assigned_task))
                        self.processor2_assigned_task = pickuped_task
                        self.processor2_busy_time = self.processor2_assigned_task.get_remaining_execution_time()
                        is_ok = False
                        while not is_ok:
                            with self.ready_queue_lock:
                                if self.reamining_resource1_number > self.processor2_assigned_task.resource1_usage and self.reamining_resource2_number > self.processor2_assigned_task.resource2_usage:
                                    self.reamining_resource1_number -= self.processor2_assigned_task.resource1_usage
                                    self.reamining_resource2_number -= self.processor2_assigned_task.resource2_usage
                                    is_ok = True
                        self.processor2_assigned_task.proceed_executed_time += 1
                        self.processor2_busy_time -= 1
                        remaining_time = self.processor2_assigned_task.get_remaining_execution_time()
                        if remaining_time <= 0: # task ended
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor2_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor2_assigned_task.resource2_usage
                            self.finished_and_aborted_tasks.append(self.processor2_assigned_task)
                            self.processor2_assigned_task = None
                            self.processor2_busy_time = 0 
                    else:
                        print("Cant Pickup a Task")
                        
                self.processor2_status = False

    

    def start_subsystem(self):
        self.move_all_tasks_to_temp_list()
        processor1_thread = threading.Thread(target=self.processor1)
        processor2_thread = threading.Thread(target=self.processor2)

        processor1_thread.start()
        processor2_thread.start()

        # Don't join here - let the thread run independently
        return