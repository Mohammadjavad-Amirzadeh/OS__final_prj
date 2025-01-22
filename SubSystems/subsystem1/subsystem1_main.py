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
        self.Ready_queue1 = queue.PriorityQueue()
        self.Ready_queue2 = queue.PriorityQueue()
        self.Ready_queue3 = queue.PriorityQueue()
        self.resource1_number = resource1_number
        self.resource2_number = resource2_number
        self.resource1_list = []
        self.resource2_list = []
        self.initiate_resources()
        self.add_to_waiting_queue()
        
        self.processor1_status = False
        self.processor2_status = False
        self.processor3_status = False
        
        self.finished_tasks = []
        
        self.subsystem1_clock = threading.Event()
        self.resource_lock = threading.Lock()
        self.waiting_queue_lock = threading.Lock()
        
        
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
                self.Ready_queue1.put((task.arrival_time, task))
            elif task.processor_number == 2:
                self.Ready_queue2.put((task.arrival_time, task))
            elif task.processor_number == 3:
                self.Ready_queue3.put((task.arrival_time, task))
            else:
                raise("WRONG PROCESSOR NUMBER DETECTED")
            task.state = 'Ready'

        
    def print_waiting_queue(self):
        print("Waiting Queue:", self.Waiting_queue.qsize())
        for _, task in list(self.Waiting_queue.queue):
            print(f"Task {task.name}, Arrival Time: {task.arrival_time}, State: {task.state}")
            
    def print_ready_queue1(self):
        print("Ready Queue 1 :")
        for _, task in list(self.Ready_queue1.queue):
            print(f"Task {task.name}, Arrival Time: {task.arrival_time}, State: {task.state}")
    
    def print_ready_queue2(self):
        print("Ready Queue 2 :")
        for _, task in list(self.Ready_queue2.queue):
            print(f"Task {task.name}, Arrival Time: {task.arrival_time}, State: {task.state}")
            
    def print_ready_queue3(self):
        print("Ready Queue 3 :")
        for _, task in list(self.Ready_queue3.queue):
            print(f"Task {task.name}, Arrival Time: {task.arrival_time}, State: {task.state}")
            
    def set_clock(self):
        self.processor1_status = True
        self.processor2_status = True
        self.processor3_status = True
        
    def is_processores_finished(self):
        return not(self.processor1_status) and not(self.processor2_status) and not(self.processor3_status)
    
    def processor1(self):
        counter = 0
        while True:
            # if counter == 10:
            #     break
            if self.processor1_status:
                with self.resource_lock:
                    time.sleep(5)
                    print('Processor 1 - COUNTER:', counter)
                    counter += 1
                    
                self.processor1_status = False
            # Clear the signal after processing 
               
    def processor2(self):
        counter = 0
        while True:
            # if counter == 10:
            #     break
            if self.processor2_status:
                with self.resource_lock:
                    time.sleep(0.3)
                    print('Processor 2 - COUNTER:', counter)
                    counter += 1
                    
                self.processor2_status = False
    
    def processor3(self):
        counter = 0
        while True:
            # if counter == 10:
            #     break
            if self.processor3_status:
                with self.resource_lock:
                    time.sleep(0.1)
                    print('Processor 3 - COUNTER:', counter)
                    counter += 1
                    
                self.processor3_status = False
    
    def start_subsystem(self):
        self.move_all_tasks_to_ready_queue()
        processor1_thread = threading.Thread(target=self.processor1)
        processor2_thread = threading.Thread(target=self.processor2)
        processor3_thread = threading.Thread(target=self.processor3)

        processor1_thread.start()
        processor2_thread.start()
        processor3_thread.start()

        # Don't join here - let the thread run independently
        return

