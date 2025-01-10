class subsystem2_task:
    def __init__(self, name, execution_time, resource1_usage, resource2_usage, arrival_time):
        self.name = name
        self.execution_time = execution_time
        self.resource1_usage = resource1_usage
        self.resource2_usage = resource2_usage
        self.arrival_time = arrival_time
        self.state = 'Waiting'