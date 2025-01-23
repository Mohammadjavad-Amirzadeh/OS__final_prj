import queue
import threading
import time
from .subsystem3_scheduler import (rate_monotonic_schedule, 
                                 is_schedulable_rm,
                                 get_next_deadline)

class subsystem3:
    def __init__(self, subsystem3_tasks):
        self.processors_count = 1
        self.Ready_queue = []  # Actually running tasks
        self.tasks = subsystem3_tasks  # All tasks including future arrivals
        self.waiting_arrivals = sorted(subsystem3_tasks, key=lambda x: x.arrival_time)
        
        self.processor_status = False
        self.processor_busy_time = 0
        self.processor_assigned_task = None
        self.quantum_task = None
        
        self.current_time = -1
        self.resource_lock = threading.Lock()
        self.completed_periods = 0
        self.missed_deadlines = 0
        
    def can_accept_task(self, new_task, current_time):
        """Determine if a new task can be accepted with current tasks"""
        test_tasks = self.Ready_queue + [new_task]
        return is_schedulable_rm(test_tasks)

    def set_clock(self):
        self.current_time += 1
        self.processor_status = True
        
        # Check for new task arrivals
        while self.waiting_arrivals and self.waiting_arrivals[0].arrival_time <= self.current_time:
            new_task = self.waiting_arrivals.pop(0)
            if self.can_accept_task(new_task, self.current_time):
                self.Ready_queue.append(new_task)
                new_task.next_deadline = new_task.arrival_time + new_task.period  # Initialize first deadline
                print(f"Accepted task {new_task.name} with period {new_task.period}, first deadline: {new_task.next_deadline}")
            else:
                print(f"Rejected task {new_task.name} - Cannot guarantee {new_task.period} period deadline")

        # Process each task's deadline
        for task in list(self.Ready_queue):  # Make copy to avoid modification during iteration
            if self.current_time >= task.next_deadline:
                if task.get_remaining_execution_time() > 0:
                    # Missed deadline
                    self.missed_deadlines += 1
                    print(f"WARNING: Task {task.name} missed deadline {task.next_deadline} at time {self.current_time}")
                else:
                    # Completed period successfully
                    self.completed_periods += 1
                    print(f"Task {task.name} completed period")

                # Handle next period
                if task.repetitions_number > 0:
                    task.repetitions_number -= 1
                    task.proceed_executed_time = 0
                    task.next_deadline = task.next_deadline + task.period
                    print(f"Task {task.name} starting new period, deadline: {task.next_deadline}")
                else:
                    print(f"Task {task.name} completed all repetitions")
                    self.Ready_queue.remove(task)

    def processor1(self):
        while True:
            if self.processor_status:
                # First check for new task to process
                if self.processor_busy_time <= 0:
                    task, deadline = rate_monotonic_schedule(self.Ready_queue, self.current_time)
                    if task and deadline > self.current_time:
                        # Remove task from ready queue when assigning it
                        self.Ready_queue.remove(task)
                        self.processor_assigned_task = task
                        self.processor_busy_time = task.get_remaining_execution_time()
                        self.quantum_task = task
                        print(f"Starting task {task.name}, deadline: {deadline}")
                        # First tick happens immediately
                        task.proceed_executed_time += 1
                        self.processor_busy_time -= 1

                # Then process current task if any
                elif self.processor_assigned_task:
                    self.quantum_task = self.processor_assigned_task
                    self.processor_assigned_task.proceed_executed_time += 1
                    self.processor_busy_time -= 1
                    
                    if self.processor_assigned_task.get_remaining_execution_time() <= 0:
                        print(f"Task {self.processor_assigned_task.name} completed execution for current period")
                        if self.processor_assigned_task.repetitions_number > 0:
                            # Put back in ready queue if there are more repetitions
                            self.Ready_queue.append(self.processor_assigned_task)
                        self.processor_assigned_task = None
                        self.processor_busy_time = 0
                        self.quantum_task = None

                self.processor_status = False

    def is_processor_finished(self):
        """Match the naming convention used in subsystem1"""
        return not self.processor_status

    def start_subsystem(self):
        processor_thread = threading.Thread(target=self.processor1)
        processor_thread.start()
        return


