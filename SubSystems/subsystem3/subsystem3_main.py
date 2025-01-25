import queue
import threading
import time
from .subsystem3_scheduler import (rate_monotonic_schedule, 
                                 is_schedulable_rm,
                                 get_next_deadline,
                                 should_preempt) 

class subsystem3:
    def __init__(self, subsystem3_tasks, resource1_number, resource2_number, main_system=None):  
        self.main_system = main_system  
        self.processors_count = 1
        self.resource1_number = resource1_number
        self.resource2_number = resource2_number
        self.Ready_queue = []  
        self.tasks = subsystem3_tasks  
        self.waiting_arrivals = sorted(subsystem3_tasks, key=lambda x: x.arrival_time)
        
        self.processor_status = False
        self.processor_busy_time = 0
        self.processor_assigned_task = None
        self.quantum_task = None
        self.just_completed = None  
        
        self.current_time = -1
        self.resource_lock = threading.Lock()
        self.completed_periods = 0
        self.finished_tasks = [] 
        self.rejected_tasks = []
        
    def can_accept_task(self, new_task, current_time):
        """Determine if a new task can be accepted with current tasks"""
        test_tasks = self.Ready_queue + [new_task]
        return is_schedulable_rm(test_tasks)

    def request_resources_from_main(self, r1_needed, r2_needed):
        """Wrapper to call main system's request_resources function"""
        if self.main_system:
            return self.main_system.request_resources(r1_needed, r2_needed)
        return False, {'sub1': (0, 0), 'sub2': (0, 0)}  

    def set_clock(self):
        self.current_time += 1
        self.processor_status = True
        
        # Check for new task arrivals
        while self.waiting_arrivals and self.waiting_arrivals[0].arrival_time <= self.current_time:
            new_task = self.waiting_arrivals.pop(0)
            if new_task.is_accepted is None:  # Only check acceptance for first arrival
                # Try regular acceptance first
                regular_schedulable = self.can_accept_task(new_task, self.current_time)
                has_local_resources = (new_task.resource1_usage <= self.resource1_number and 
                                     new_task.resource2_usage <= self.resource2_number)
                
                if regular_schedulable and has_local_resources:
                    new_task.is_accepted = True
                    self.Ready_queue.append(new_task)
                    new_task.next_deadline = new_task.arrival_time + new_task.period
                    print(f"First arrival: Accepted task {new_task.name} with period {new_task.period}, deadline: {new_task.next_deadline}")
                else:
                    # Try speedup before rejecting
                    print(f"Task {new_task.name} needs speedup, attempting to request additional resources...")
                    success, allocated = self.request_resources_from_main(new_task.resource1_usage, new_task.resource2_usage)
                    
                    if success:
                        # Test schedulability with halved execution time
                        original_exec_time = new_task.execution_time
                        new_task.execution_time = original_exec_time / 2
                        speedup_schedulable = self.can_accept_task(new_task, self.current_time)
                        
                        if speedup_schedulable:
                            print(f"Speedup successful for {new_task.name}! New execution time: {new_task.execution_time}")
                            new_task.is_accepted = True
                            new_task.speedup_needed = True
                            new_task.speedup_resources = allocated
                            self.Ready_queue.append(new_task)
                            new_task.next_deadline = new_task.arrival_time + new_task.period
                        else:
                            print(f"Even with speedup, {new_task.name} cannot meet deadlines")
                            new_task.execution_time = original_exec_time  # Restore original execution time
                            new_task.is_accepted = False
                            self.rejected_tasks.append(new_task)
                    else:
                        print(f"Could not get additional resources for {new_task.name}")
                        new_task.is_accepted = False
                        self.rejected_tasks.append(new_task)
            else:  # For subsequent arrivals
                if new_task.is_accepted:
                    self.Ready_queue.append(new_task)
                    new_task.next_deadline = new_task.arrival_time + new_task.period
                    print(f"Next period: Task {new_task.name} added to ready queue, deadline: {new_task.next_deadline}")

        # Reset burst completion flag for all tasks at period boundaries
        for task in list(self.Ready_queue):
            if self.current_time >= task.next_deadline:
                task.current_burst_complete = False
                task.next_deadline = task.next_deadline + task.period
                print(f"Task {task.name} starting new period, deadline: {task.next_deadline}")

    def processor1(self):
        while True:
            if self.processor_status:
                # First check if current task should be preempted
                if self.processor_assigned_task and self.Ready_queue:
                    if should_preempt(self.processor_assigned_task, self.Ready_queue):
                        print(f"Preempting task {self.processor_assigned_task.name}")
                        # Put current task back in ready queue
                        self.Ready_queue.append(self.processor_assigned_task)
                        self.processor_assigned_task = None
                        self.processor_busy_time = 0

                # Then process or get new task
                if self.processor_busy_time <= 0:
                    task, deadline = rate_monotonic_schedule(self.Ready_queue, self.current_time)
                    if task and deadline > self.current_time:
                        self.Ready_queue.remove(task)
                        self.processor_assigned_task = task
                        self.processor_busy_time = task.get_remaining_execution_time()
                        self.quantum_task = task
                        print(f"Starting task {task.name}, deadline: {deadline}")
                        task.proceed_executed_time += 1
                        self.processor_busy_time -= 1
                        #چك اتمام
                        if self.processor_assigned_task.get_remaining_execution_time() <= 0:
                            self.processor_assigned_task.current_burst_complete = True
                            self.just_completed = self.processor_assigned_task  # Store the just completed task
                            print(f"\n>>> Task {self.processor_assigned_task.name} COMPLETED BURST for current period <<<\n")
                            self.completed_periods += 1
                            
                            if self.processor_assigned_task.repetitions_number > 0:
                                self.processor_assigned_task.repetitions_number -= 1
                                if self.processor_assigned_task.repetitions_number > 0:
                                    # Calculate next arrival and put in waiting_arrivals
                                    task = self.processor_assigned_task
                                    task.proceed_executed_time = 0
                                    task.current_burst_complete = False
                                    # Fix: Next arrival should be based on first arrival plus period multiples
                                    periods_completed = (self.current_time - task.arrival_time) // task.period
                                    task.arrival_time = task.arrival_time + (periods_completed + 1) * task.period
                                    
                                    # Insert into waiting_arrivals maintaining sort
                                    insert_idx = 0
                                    for idx, t in enumerate(self.waiting_arrivals):
                                        if t.arrival_time > task.arrival_time:
                                            break
                                        insert_idx = idx + 1
                                    self.waiting_arrivals.insert(insert_idx, task)
                                    print(f"Task {task.name} scheduled for next arrival at {task.arrival_time}")
                                else:
                                    if self.processor_assigned_task.speedup_needed:
                                        print("sped up task finished")
                                        print("Releasing speedup resources")
                                        self.main_system.release_resources(self.processor_assigned_task.speedup_resources)
                                    self.finished_tasks.append(self.processor_assigned_task)
                                    
                            self.processor_assigned_task = None
                            self.processor_busy_time = 0

                elif self.processor_assigned_task:
                    self.quantum_task = self.processor_assigned_task
                    self.processor_assigned_task.proceed_executed_time += 1
                    self.processor_busy_time -= 1
                    
                    if self.processor_assigned_task.get_remaining_execution_time() <= 0:
                        self.processor_assigned_task.current_burst_complete = True
                        self.just_completed = self.processor_assigned_task  # Store the just completed task
                        print(f"\n>>> Task {self.processor_assigned_task.name} COMPLETED BURST for current period <<<\n")
                        self.completed_periods += 1
                        
                        if self.processor_assigned_task.repetitions_number > 0:
                            self.processor_assigned_task.repetitions_number -= 1
                            if self.processor_assigned_task.repetitions_number > 0:
                                # Calculate next arrival and put in waiting_arrivals
                                task = self.processor_assigned_task
                                task.proceed_executed_time = 0
                                task.current_burst_complete = False
                                # Fix: Next arrival should be based on first arrival plus period multiples
                                periods_completed = (self.current_time - task.arrival_time) // task.period
                                task.arrival_time = task.arrival_time + (periods_completed + 1) * task.period
                                
                                # Insert into waiting_arrivals maintaining sort
                                insert_idx = 0
                                for idx, t in enumerate(self.waiting_arrivals):
                                    if t.arrival_time > task.arrival_time:
                                        break
                                    insert_idx = idx + 1
                                self.waiting_arrivals.insert(insert_idx, task)
                                print(f"Task {task.name} scheduled for next arrival at {task.arrival_time}")
                            else:
                                if self.processor_assigned_task.speedup_needed:
                                    print("Releasing speedup resources")
                                    self.main_system.release_resources(self.processor_assigned_task.speedup_resources)

                                self.finished_tasks.append(self.processor_assigned_task)
                                
                        self.processor_assigned_task = None
                        self.processor_busy_time = 0
                        # Don't clear quantum_task here, let it persist for one more cycle

                self.processor_status = False

    def is_processor_finished(self):
        """Match the naming convention used in subsystem1"""
        return not self.processor_status

    def start_subsystem(self):
        processor_thread = threading.Thread(target=self.processor1)
        processor_thread.start()
        return

