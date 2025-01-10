class subsystem1_task:
    def __init__(self, name: str, execution_time: int, resource1_usage: int, resource2_usage: int, arrival_time: int, processor_number: int):
        self.name = name
        self.execution_time = execution_time
        self.resource1_usage = resource1_usage
        self.resource2_usage = resource2_usage
        self.arrival_time = arrival_time
        self.processor_number = processor_number
        self.state = 'Waiting'
        self.proceed_execution_time = 0
        self.remaining_execution_time = self.execution_time - self.proceed_execution_time
        
    
    def update_remaining_execution_time():
        self.remaining_execution_time = self.execution_time - self.proceed_execution_time
        
    def __lt__(self, other):
        return self.arrival_time < other.arrival_time
