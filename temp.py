class Task:
    def __init__(self, task_id, execution_time):
        self.task_id = task_id
        self.execution_time = execution_time
        self.remaining_time = execution_time

class WeightedRoundRobinScheduler:
    def __init__(self):
        self.ready_queue = []

    def add_task(self, task_id, execution_time):
        task = Task(task_id, execution_time)
        self.ready_queue.append(task)

    def schedule(self, time_slice):
        print("Starting Weighted Round Robin Scheduling")
        while any(task.remaining_time > 0 for task in self.ready_queue):
            for task in self.ready_queue:
                if task.remaining_time > 0:
                    # Calculate weighted time slice
                    weighted_slice = time_slice * task.execution_time

                    # Process the task
                    process_time = min(weighted_slice, task.remaining_time)
                    task.remaining_time -= process_time

                    print(f"Task {task.task_id}: Processed for {process_time} units, Remaining time: {task.remaining_time}")

# Example usage
if __name__ == "__main__":
    scheduler = WeightedRoundRobinScheduler()

    # Adding tasks with execution times
    scheduler.add_task(task_id=1, execution_time=5)
    scheduler.add_task(task_id=2, execution_time=3)
    scheduler.add_task(task_id=3, execution_time=8)

    # Define base time slice
    base_time_slice = 1 / 4

    # Start scheduling
    scheduler.schedule(time_slice=base_time_slice)
