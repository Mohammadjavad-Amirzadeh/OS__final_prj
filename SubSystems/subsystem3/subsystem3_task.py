class subsystem3_task:
    def __init__(self, name, execution_time, resource1_usage, resource2_usage, arrival_time, period, repetitions_number):
        self.name = name
        self.execution_time = execution_time
        self.resource1_usage = resource1_usage
        self.resource2_usage = resource2_usage
        self.arrival_time = arrival_time
        self.period = period
        self.repetitions_number = repetitions_number
        self.state = 'Waiting'
        self.speedup_needed = False  # Track if task needs speedup
        self.proceed_executed_time = 0
        self.next_deadline = arrival_time + period
        
    def get_remaining_execution_time(self):
        return self.execution_time - self.proceed_executed_time

    def update_deadline(self, current_time):
        if current_time >= self.next_deadline:
            self.next_deadline += self.period
            return True
        return False

    def __str__(self):
        return f"Task {self.name} (Remaining: {self.get_remaining_execution_time()}, Next deadline: {self.next_deadline})"