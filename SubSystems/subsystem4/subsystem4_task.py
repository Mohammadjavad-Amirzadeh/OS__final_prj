from Resources.Resource1 import resource1
from Resources.Resource2 import resource2


class subsystem4_task:
    def __init__(self, name: str, execution_time: int, resource1_usage: int, resource2_usage: int, arrival_time: int, pretask: str):
        self.name = name
        self.execution_time = execution_time
        self.resource1_usage = resource1_usage  # total resource one to work
        self.resource2_usage = resource2_usage  # total resource two to work
        self.arrival_time = arrival_time
        self.state = 'Waiting'
        self.prerequisite_task = pretask
        self.proceed_executed_time = 0
        self.remaining_execution_time = self.execution_time - self.proceed_executed_time
        
    
    def get_remaining_execution_time(self):
        self.remaining_execution_time = self.execution_time - self.proceed_executed_time
        return self.remaining_execution_time
        
    def __lt__(self, other):
        return self.arrival_time < other.arrival_time

    def __str__(self):
        return f"Task {self.name} (Remaining: {self.get_remaining_execution_time()})"
