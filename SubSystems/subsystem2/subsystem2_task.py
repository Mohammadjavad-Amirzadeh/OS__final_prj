class subsystem2_task:
    def __init__(self, name, execution_time, resource1_usage, resource2_usage, arrival_time):
        self.name = name
        self.execution_time = execution_time
        self.resource1_usage = resource1_usage
        self.resource2_usage = resource2_usage
        self.arrival_time = arrival_time
        self.state = 'Waiting'
        
        self.proceed_executed_time = 0
        self.remaining_execution_time = self.execution_time - self.proceed_executed_time
        
    def get_remaining_execution_time(self):
        self.remaining_execution_time = self.execution_time - self.proceed_executed_time
        return self.remaining_execution_time
    
    def __lt__(self, other):
        return self.arrival_time < other.arrival_time

    def __str__(self):
        return f"Task {self.name} (Remaining: {self.get_remaining_execution_time()})"