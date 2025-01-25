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
        self.is_accepted = None  # New flag to track if task has been accepted
        self.current_burst_complete = False  # New flag to track burst completion
        self.speedup_resources = None
        
    def get_remaining_execution_time(self):
        return self.execution_time - self.proceed_executed_time

    def update_deadline(self, current_time):
        if current_time >= self.next_deadline:
            self.next_deadline += self.period
            return True
        return False

    def __str__(self):
        status = "BURST COMPLETE" if self.current_burst_complete else f"Remaining: {self.get_remaining_execution_time()}"
        acceptance = "Accepted" if self.is_accepted else "Rejected" if self.is_accepted is not None else "Pending"
        return f"Task {self.name} ({status}, Next deadline: {self.next_deadline}, {acceptance})"