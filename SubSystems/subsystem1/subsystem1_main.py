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
        
        self.lock = threading.Lock()
        
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
        
    def processor1():
        pass
    
    def processor2():
        pass
    
    def processor3():
        pass
    
    def start_subsystem(self):
        self.move_all_tasks_to_ready_queue()
        
        pass        
