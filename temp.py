# Resource Class
class Resource:
    def __init__(self, resource_id):
        self.resource_id = resource_id
        self.is_available = True

    def allocate(self):
        if self.is_available:
            self.is_available = False
            return True
        return False

    def release(self):
        self.is_available = True


# Task Class
class Task:
    def __init__(self, task_id, execution_time, deadline=None, required_resources=None):
        self.task_id = task_id
        self.execution_time = execution_time
        self.state = "Ready"
        self.deadline = deadline
        self.required_resources = required_resources if required_resources else []

    def update_state(self, new_state):
        self.state = new_state


# Queue Class
class Queue:
    def __init__(self, queue_type):
        self.tasks = []
        self.queue_type = queue_type

    def enqueue(self, task):
        self.tasks.append(task)

    def dequeue(self):
        if self.tasks:
            return self.tasks.pop(0)
        return None

    def sort_queue(self, key_func):
        self.tasks.sort(key=key_func)


# Processor Class
class Processor:
    def __init__(self, processor_id):
        self.processor_id = processor_id
        self.current_task = None
        self.ready_queue = Queue("Ready")
        self.waiting_queue = Queue("Waiting")

    def assign_task(self, task):
        self.current_task = task
        task.update_state("Running")

    def execute_task(self):
        if self.current_task:
            self.current_task.execution_time -= 1
            if self.current_task.execution_time <= 0:
                self.current_task = None

    def handle_waiting_queue(self):
        for task in self.waiting_queue.tasks:
            if all(res.is_available for res in task.required_resources):
                for res in task.required_resources:
                    res.allocate()
                self.waiting_queue.tasks.remove(task)
                self.ready_queue.enqueue(task)


# Scheduler Class
class Scheduler:
    def __init__(self, processors):
        self.processors = processors

    def assign_tasks(self):
        for processor in self.processors:
            if not processor.current_task and processor.ready_queue.tasks:
                next_task = processor.ready_queue.dequeue()
                processor.assign_task(next_task)

    def monitor(self):
        for processor in self.processors:
            print(f"Processor {processor.processor_id} running task: {processor.current_task.task_id if processor.current_task else 'None'}")

    def resolve_deadlock(self):
        # Implement deadlock resolution logic if necessary
        pass


# Main System Class
class MainSystem:
    def __init__(self, resources, processors):
        self.resources = resources
        self.processors = processors

    def run_simulation(self):
        scheduler = Scheduler(self.processors)
        while True:  # Replace with a condition to stop the simulation
            for processor in self.processors:
                processor.execute_task()
                processor.handle_waiting_queue()
            scheduler.assign_tasks()
            scheduler.monitor()
            # Add any termination conditions or simulation logic
            break


# Example usage
if __name__ == "__main__":
    # Create resources
    resources = [Resource("R1"), Resource("R2")]

    # Create processors
    processors = [Processor(1), Processor(2), Processor(3)]

    # Create tasks
    tasks = [
        Task("T1", execution_time=5, required_resources=[resources[0]]),
        Task("T2", execution_time=3, required_resources=[resources[1]]),
        Task("T3", execution_time=7),
    ]

    # Add tasks to ready queues
    processors[0].ready_queue.enqueue(tasks[0])
    processors[1].ready_queue.enqueue(tasks[1])
    processors[2].ready_queue.enqueue(tasks[2])

    # Run simulation
    system = MainSystem(resources, processors)
    system.run_simulation()
