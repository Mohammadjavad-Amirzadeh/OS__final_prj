import time
import math
import queue 
import random
import threading
from SubSystems.subsystem4.subsystem4_task import subsystem4_task


class subsystem4:
    def __init__(self, subsystem4_tasks, resource1_number, resource2_number, main_system):
        self.subsystem_number = 4
        self.processors_count = 2
        self.tasks = subsystem4_tasks
        self.Waiting_queue = []
        self.storing_all_tasks = queue.PriorityQueue()
        self.Ready_queue = []
        self.resource1_number = resource1_number
        self.resource2_number = resource2_number
        self.reamining_resource1_number = resource1_number
        self.reamining_resource2_number = resource2_number

        self.add_to_storing_all_tasks()
        
        self.processor1_status = False
        self.processor2_status = False
        
        self.processor1_busy_time = 0
        self.processor2_busy_time = 0
        
        self.processor1_assigned_task = None
        self.processor2_assigned_task = None
        
        self.processor1_is_ok = False
        self.processor2_is_ok = False
        
        self.finished_tasks = [None]
        
        self.subsystem_did = {'processor1': 'IDLE',
                              'processor2': 'IDLE'}
        
        self.subsystem1_clock = threading.Event()
        self.resource_lock = threading.Lock()
        self.waiting_queue_lock = threading.Lock()
        self.ready_queue_lock = threading.Lock()
        self.execution_lock = threading.Lock()
        self.current_time = -1
        self.main_system = main_system
    
    def add_to_storing_all_tasks(self):
        for task in self.tasks:
            self.storing_all_tasks.put((task.arrival_time, task))

    def check_add_task_by_arrival_time(self):
        storing_tasks = []
        while not self.storing_all_tasks.empty():
            storing_tasks.append(self.storing_all_tasks.get())
        for arrival, task in storing_tasks:
            if arrival <= self.current_time:
                print(f"SUBSYSTEM 4 : {task} MOVE TO READY QUEUE")
                self.Ready_queue.append(task)
            else:
                self.storing_all_tasks.put((arrival, task))
    
    def check_can_assign_resource(self, task):
        if task.resource1_usage <= self.reamining_resource1_number and task.resource2_usage <= self.reamining_resource2_number:
            return True
        else:
            return False
    
    def move_from_waiting_queue_to_ready_queue(self):
        with self.ready_queue_lock and self.waiting_queue_lock:
            counter = len(self.Waiting_queue)
            temp = []
            while len(self.Waiting_queue):
                self.Ready_queue.append(self.Waiting_queue.pop(0))

    def set_clock(self):
        self.current_time += 1  # Add this line to increment time
        self.check_add_task_by_arrival_time()
        if self.current_time != 0 and self.current_time % 2 == 0:
            self.move_from_waiting_queue_to_ready_queue()
        self.processor1_status = True
        self.processor2_status = True
    
    def is_processores_finished(self):
        return not(self.processor1_status) and not(self.processor2_status)
    
    def probability_of_error(self):
        return random.randint(1, 10) <= 3
    
    def processor1(self):
        while True:
            if self.processor1_status:
                if self.processor1_busy_time > 0:
                    if self.processor1_assigned_task:
                        '''
                        resuming the process run
                        '''
                        has_error = self.probability_of_error()
                        if has_error:
                            self.subsystem_did['processor1'] = 'IDLE'
                            print(f"SUBSYSTEM 4 : THIS TASK GET ERRORED => {self.processor1_assigned_task} WHILE EXECUTING IN PROCESSOR 1")
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor1_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor1_assigned_task.resource2_usage
                            with self.ready_queue_lock:
                                self.Ready_queue.append(self.processor1_assigned_task)
                            self.processor1_assigned_task.proceed_executed_time = 0
                            self.processor1_assigned_task = None
                            self.processor1_busy_time = 0
                        else:
                            # EXECUTION 
                            self.subsystem_did['processor1'] = self.processor1_assigned_task
                            self.processor1_assigned_task.proceed_executed_time += 1
                            self.processor1_busy_time -= 1
                            remaining_time = self.processor1_assigned_task.get_remaining_execution_time()
                            if remaining_time <= 0:
                                with self.resource_lock:
                                    self.reamining_resource1_number += self.processor1_assigned_task.resource1_usage
                                    self.reamining_resource2_number += self.processor1_assigned_task.resource2_usage
                                with self.execution_lock:
                                    self.finished_tasks.append(self.processor1_assigned_task)
                                    self.main_system.execution_tracker.task_finished(
                                        self.processor1_assigned_task.name,
                                        self.current_time,
                                        self.processor1_assigned_task.proceed_executed_time,
                                        "subsystem4_core1"
                                    )
                                self.processor1_assigned_task = None
                                self.processor1_busy_time = 0
                elif self.processor1_busy_time <= 0:
                    '''
                    choose new task for run
                    '''
                    new_task = None
                    is_task_in_ready_queue = False
                    temp_task = None
                    assign_resource = False
                    is_prerequisite_task_done = False
                    with self.ready_queue_lock:
                        while len(self.Ready_queue) > 0:
                            temp_task = self.Ready_queue.pop(0)
                            is_task_in_ready_queue = True
                            break
                    if is_task_in_ready_queue:
                        with self.resource_lock and self.execution_lock and self.waiting_queue_lock:
                            if temp_task.resource1_usage <= self.reamining_resource1_number and temp_task.resource2_usage <= self.reamining_resource2_number:
                                assign_resource = True
                            else:
                                print(f"SUBSYSTEM 4 : TASK {temp_task} MOVED TO WAITING QUEUE BECAUSE RESOURCES ARE NOT COMPLETE IN PROCESSOR 1")
                                assign_resource = False
                            finished_task_names = [task.name for task in self.finished_tasks if task is not None]
                            if assign_resource and ((temp_task.prerequisite_task in finished_task_names) or temp_task.prerequisite_task == None):
                                new_task = temp_task
                                is_prerequisite_task_done = True
                                assign_resource = True
                            else:
                                print(f"SUBSYSTEM 4 : TASK {temp_task} MOVED TO WAITING QUEUE BECAUSE RESOURCES OR PREREQUISITE ARE NOT COMPLETE IN PROCESSOR 1")
                                assign_resource = False
                                is_prerequisite_task_done = False
                            if assign_resource and is_prerequisite_task_done:
                                self.reamining_resource1_number -= temp_task.resource1_usage
                                self.reamining_resource2_number -= temp_task.resource2_usage
                            else:
                                self.Waiting_queue.append(temp_task)
                                
                        if assign_resource and is_prerequisite_task_done and new_task:
                            self.processor1_assigned_task = new_task
                            self.processor1_busy_time = self.processor1_assigned_task.get_remaining_execution_time()
                            print(f"SUBSYSTEM 4 : THIS TASK CHOOSED => {self.processor1_assigned_task} AND ITS PRETASK = {self.processor1_assigned_task. prerequisite_task}")
                            has_error = self.probability_of_error()
                            if has_error:
                                self.subsystem_did['processor1'] = 'IDLE'
                                print(f"SUBSYSTEM 4 : THIS TASK GET ERRORED => {self.processor1_assigned_task} WHILE EXECUTING IN PROCESSOR 1")
                                with self.resource_lock:
                                    self.reamining_resource1_number += self.processor1_assigned_task.resource1_usage
                                    self.reamining_resource2_number += self.processor1_assigned_task.resource2_usage
                                with self.ready_queue_lock:
                                    self.Ready_queue.append(self.processor1_assigned_task)
                                self.processor1_assigned_task.proceed_executed_time = 0
                                self.processor1_assigned_task = None
                                self.processor1_busy_time = 0
                            else:
                                # EXECUTION
                                self.subsystem_did['processor1'] = self.processor1_assigned_task
                                self.processor1_assigned_task.proceed_executed_time += 1
                                self.processor1_busy_time -= 1
                                remaining_time = self.processor1_assigned_task.get_remaining_execution_time()
                                if remaining_time <= 0:
                                    with self.resource_lock:
                                        self.reamining_resource1_number += self.processor1_assigned_task.resource1_usage
                                        self.reamining_resource2_number += self.processor1_assigned_task.resource2_usage
                                    with self.execution_lock:
                                        self.finished_tasks.append(self.processor1_assigned_task)
                                        self.main_system.execution_tracker.task_finished(
                                            self.processor1_assigned_task.name,
                                            self.current_time,
                                            self.processor1_assigned_task.proceed_executed_time,
                                            "subsystem4_core1"
                                        )
                                    self.processor1_assigned_task = None
                                    self.processor1_busy_time = 0
                        else:
                            self.subsystem_did['processor1'] = 'IDLE'
                    else:
                        self.subsystem_did['processor1'] = 'IDLE'
                        print('SUBSYSTEM 4 : READY QUEUE IS EMPTY')
                            
                self.processor1_status = False

    def processor2(self):
        while True:
            if self.processor2_status:
                if self.processor2_busy_time > 0:
                    if self.processor2_assigned_task:
                        '''
                        resuming the process run
                        '''
                        has_error = self.probability_of_error()
                        if has_error:
                            self.subsystem_did['processor2'] = 'IDLE'
                            print(f"SUBSYSTEM 4 : THIS TASK GET ERRORED => {self.processor2_assigned_task} WHILE EXECUTING IN PROCESSOR 2")
                            with self.resource_lock:
                                self.reamining_resource1_number += self.processor2_assigned_task.resource1_usage
                                self.reamining_resource2_number += self.processor2_assigned_task.resource2_usage
                            with self.ready_queue_lock:
                                self.Ready_queue.append(self.processor2_assigned_task)
                            self.processor2_assigned_task.proceed_executed_time = 0
                            self.processor2_assigned_task = None
                            self.processor2_busy_time = 0
                        else:
                            # EXECUTION 
                            self.subsystem_did['processor2'] = self.processor2_assigned_task
                            self.processor2_assigned_task.proceed_executed_time += 1
                            self.processor2_busy_time -= 1
                            remaining_time = self.processor2_assigned_task.get_remaining_execution_time()
                            if remaining_time <= 0:
                                with self.resource_lock:
                                    self.reamining_resource1_number += self.processor2_assigned_task.resource1_usage
                                    self.reamining_resource2_number += self.processor2_assigned_task.resource2_usage
                                with self.execution_lock:
                                    self.finished_tasks.append(self.processor2_assigned_task)
                                    self.main_system.execution_tracker.task_finished(
                                        self.processor2_assigned_task.name,
                                        self.current_time,
                                        self.processor2_assigned_task.proceed_executed_time,
                                        "subsystem4_core2"
                                    )
                                self.processor2_assigned_task = None
                                self.processor2_busy_time = 0
                            
                elif self.processor2_busy_time <= 0:
                    '''
                    choose new task for run
                    '''
                    new_task = None
                    temp_task = None
                    assign_resource = False
                    is_prerequisite_task_done = False
                    with self.ready_queue_lock:
                        while len(self.Ready_queue) > 0:
                            temp_task = self.Ready_queue.pop(0)
                            is_task_in_ready_queue = True
                            break
                    if temp_task:
                        with self.resource_lock and self.execution_lock and self.waiting_queue_lock:
                            if temp_task.resource1_usage <= self.reamining_resource1_number and temp_task.resource2_usage <= self.reamining_resource2_number:
                                assign_resource = True
                            else:
                                print(f"SUBSYSTEM 4 : TASK {temp_task} MOVED TO WAITING QUEUE BECAUSE RESOURCES ARE NOT COMPLETE IN PROCESSOR 2")
                                assign_resource = False
                            finished_task_names = [task.name for task in self.finished_tasks if task is not None]
                            if assign_resource and ((temp_task.prerequisite_task in finished_task_names) or temp_task.prerequisite_task == None):
                                new_task = temp_task
                                is_prerequisite_task_done = True
                                assign_resource = True
                            else:
                                print(f"SUBSYSTEM 4 : TASK {temp_task} MOVED TO WAITING QUEUE BECAUSE RESOURCES OR PREREQUISITE ARE NOT COMPLETE IN PROCESSOR 2")
                                assign_resource = False
                                is_prerequisite_task_done = False
                            if assign_resource and is_prerequisite_task_done:
                                self.reamining_resource1_number -= temp_task.resource1_usage
                                self.reamining_resource2_number -= temp_task.resource2_usage
                            else:
                                self.Waiting_queue.append(temp_task)
                                
                        if assign_resource and is_prerequisite_task_done and new_task:
                            self.processor2_assigned_task = new_task
                            self.processor2_busy_time = self.processor2_assigned_task.get_remaining_execution_time()
                            print(f"SUBSYSTEM 4 : THIS TASK CHOOSED => {self.processor2_assigned_task} AND ITS PRETASK = {self.processor2_assigned_task. prerequisite_task}")
                            has_error = self.probability_of_error()
                            if has_error:
                                self.subsystem_did['processor2'] = 'IDLE'
                                print(f"SUBSYSTEM 4 : THIS TASK GET ERRORED => {self.processor2_assigned_task} WHILE EXECUTING IN PROCESSOR 2")
                                with self.resource_lock:
                                    self.reamining_resource1_number += self.processor2_assigned_task.resource1_usage
                                    self.reamining_resource2_number += self.processor2_assigned_task.resource2_usage
                                with self.ready_queue_lock:
                                    self.Ready_queue.append(self.processor2_assigned_task)
                                self.processor2_assigned_task.proceed_executed_time = 0
                                self.processor2_assigned_task = None
                                self.processor2_busy_time = 0
                            else:
                                # EXECUTION
                                self.subsystem_did['processor2'] = self.processor2_assigned_task
                                self.processor2_assigned_task.proceed_executed_time += 1
                                self.processor2_busy_time -= 1
                                remaining_time = self.processor2_assigned_task.get_remaining_execution_time()
                                if remaining_time <= 0:
                                    with self.resource_lock:
                                        self.reamining_resource1_number += self.processor2_assigned_task.resource1_usage
                                        self.reamining_resource2_number += self.processor2_assigned_task.resource2_usage
                                    with self.execution_lock:
                                        self.finished_tasks.append(self.processor2_assigned_task)
                                        self.main_system.execution_tracker.task_finished(
                                            self.processor2_assigned_task.name,
                                            self.current_time,
                                            self.processor2_assigned_task.proceed_executed_time,
                                            "subsystem4_core2"
                                        )
                                    self.processor2_assigned_task = None
                                    self.processor2_busy_time = 0
                        else:
                            self.subsystem_did['processor2'] = 'IDLE'
                    else:
                        self.subsystem_did['processor2'] = 'IDLE'
                        print("SUBSYSTEM 4 : READY QUEUE IS EMPTY") 
                                   
                self.processor2_status = False
                
    def start_subsystem(self):
        processor1_thread = threading.Thread(target=self.processor1)
        processor2_thread = threading.Thread(target=self.processor2)

        processor1_thread.start()
        processor2_thread.start()

        # Don't join here - let the thread run independently
        return