from Resources.Resource1 import resource1
from Resources.Resource2 import resource2


class subsystem1_task:
    def __init__(self, name: str, execution_time: int, resource1_usage: int, resource2_usage: int, arrival_time: int, processor_number: int):
        self.name = name
        self.execution_time = execution_time
        self.resource1_usage = resource1_usage  # total resource one to work
        self.resource2_usage = resource2_usage  # total resource two to work
        self.arrival_time = arrival_time
        self.processor_number = processor_number
        self.state = 'Waiting'
        # self.using_resource1_number = 0 # number of resource one reached
        # self.using_resource2_number = 0 # number of resource two reached
        # self.using_resource1_list = []  # list of resource one reached
        # self.using_resource2_list = []  # list of resource one reached
        self.proceed_executed_time = 0
        self.remaining_execution_time = self.execution_time - self.proceed_executed_time
        
    
    def get_remaining_execution_time(self):
        self.remaining_execution_time = self.execution_time - self.proceed_executed_time
        return self.remaining_execution_time
        
    # def append_to_using_resource1_list(self, resource: resource1, resource_number):
    #     if resource_number == 1:
    #         self.using_resource1_list.append(resource)
    #     else:
    #         raise('WRONG RESOURCE NUMBER')
            
    # def append_to_using_resource1_list(self, resource: resource2, resource_number):
    #     if resource_number == 2:
    #         self.using_resource1_list.append(resource)
    #     else:
    #         raise('WRONG RESOURCE NUMBER')
        
    def __lt__(self, other):
        return self.arrival_time < other.arrival_time
