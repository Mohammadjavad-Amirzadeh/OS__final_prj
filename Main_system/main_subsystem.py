import threading
from Main_system.get_input import get_input
from SubSystems.subsystem1.subsystem1_task import subsystem1_task
from SubSystems.subsystem1.subsystem1_main import subsystem1
from SubSystems.subsystem3.subsystem3_task import subsystem3_task
from SubSystems.subsystem3.subsystem3_main import subsystem3
from SubSystems.subsystem2.subsystem2_task import subsystem2_task
from SubSystems.subsystem2.subsystem2_main import subsystem2
from SubSystems.subsystem4.subsystem4_task import subsystem4_task
from SubSystems.subsystem4.subsystem4_main import subsystem4
import time
from Reports.execution_tracker import ExecutionTracker

class main_subsystem:
        
    def request_resources(self, r1_needed, r2_needed):
        with self.SUB1.resource_lock and self.SUB2.resource_lock :
            remaining_sub1_1 = self.SUB1.reamining_resource1_number
            remaining_sub1_2 = self.SUB1.reamining_resource2_number
            remaining_sub2_1 = self.SUB2.reamining_resource1_number
            remaining_sub2_2 = self.SUB2.reamining_resource2_number
            if r1_needed <= remaining_sub1_1 + remaining_sub2_1 and r2_needed <= remaining_sub1_2 + remaining_sub2_2:
                allocated_from_sub1_1 = min(r1_needed, remaining_sub1_1)
                allocated_from_sub1_2 = min(r2_needed, remaining_sub1_2)
                allocated_from_sub2_1 = min(r1_needed - allocated_from_sub1_1, remaining_sub2_1)
                allocated_from_sub2_2 = min(r2_needed - allocated_from_sub1_2, remaining_sub2_2)
                self.SUB1.reamining_resource1_number -= allocated_from_sub1_1
                self.SUB2.reamining_resource1_number -= allocated_from_sub2_1
                self.SUB1.reamining_resource2_number -= allocated_from_sub1_2
                self.SUB2.reamining_resource2_number -= allocated_from_sub2_2
                allcoted = {}
                allcoted['sub1'] = (allocated_from_sub1_1, allocated_from_sub1_2)
                allcoted['sub2'] = (allocated_from_sub2_1, allocated_from_sub2_2)
                print(f"Resources for speedup allocated successfully sub1_resource1: {allocated_from_sub1_1}, sub1_resource2: {allocated_from_sub1_2}, sub2_resource1: {allocated_from_sub2_1}, sub2_resource2: {allocated_from_sub2_2}")
                return True, allcoted
            else:
                allcoted  ['sub1'] = (0, 0)
                allcoted  ['sub2'] = (0, 0)
                return False, allcoted
            
    def release_resources(self, spedup_resources):
        with self.SUB1.resource_lock and self.SUB2.resource_lock :
            self.SUB1.reamining_resource1_number += spedup_resources['sub1'][0]
            self.SUB2.reamining_resource1_number += spedup_resources['sub2'][0]
            self.SUB1.reamining_resource2_number += spedup_resources['sub1'][1]
            self.SUB2.reamining_resource2_number += spedup_resources['sub2'][1]
                

    def run(self):
        self.execution_tracker = ExecutionTracker()
        subsystems_threads = []
        # Update get_input() call to include sub4 params
        (sub1_tasks_dict, sub2_tasks_dict, sub3_tasks_dict, sub4_tasks_dict,
         sub1_r1, sub1_r2, sub2_r1, sub2_r2, sub3_r1, sub3_r2, sub4_r1, sub4_r2) = get_input()
        
        # Initialize subsystem 1
        sub1_tasks = []
        for task in sub1_tasks_dict:
            temp_task = subsystem1_task(task['name'], task['execution_time'],
                                    task['resource1_usage'], task['resource2_usage'],
                                    task['arrival_time'], task['processor_number'])
            sub1_tasks.append(temp_task)
        
        #Initialize subsystem 2
        sub2_tasks = []
        for task in sub2_tasks_dict:
            temp_task = subsystem2_task(task['name'], task['execution_time'],
                                    task['resource1_usage'], task['resource2_usage'],
                                    task['arrival_time'])
            sub2_tasks.append(temp_task)
        
        # Initialize subsystem 3
        sub3_tasks = []
        for task in sub3_tasks_dict:
            temp_task = subsystem3_task(task['name'], task['execution_time'],
                                    task['resource1_usage'], task['resource2_usage'],
                                    task['arrival_time'], task['period'],
                                    task['repetitions_number'])
            sub3_tasks.append(temp_task)
        
        # Initialize subsystem 4
        sub4_tasks = []
        for task in sub4_tasks_dict:
            temp_task = subsystem4_task(task['name'], task['execution_time'],
                                    task['resource1_usage'], task['resource2_usage'],
                                    task['arrival_time'], task['prerequisite_task'])
            sub4_tasks.append(temp_task)

        for task in sub1_tasks:
            self.execution_tracker.add_task(task.name, task.arrival_time, "subsystem1")
        for task in sub2_tasks:
            self.execution_tracker.add_task(task.name, task.arrival_time, "subsystem2")
        for task in sub3_tasks:
            self.execution_tracker.add_task(task.name, task.arrival_time, "subsystem3")
        for task in sub4_tasks:
            self.execution_tracker.add_task(task.name, task.arrival_time, "subsystem4")

        SUB1 = subsystem1(sub1_tasks, sub1_r1, sub1_r2, self)
        SUB2 = subsystem2(sub2_tasks, sub2_r1, sub2_r2, self)
        SUB3 = subsystem3(sub3_tasks, sub3_r1, sub3_r2, self)  # Pass self reference
        SUB4 = subsystem4(sub4_tasks, sub4_r1, sub4_r2, self)

        self.SUB1 = SUB1
        self.SUB2 = SUB2
        self.SUB3 = SUB3
        self.SUB4 = SUB4

        
        print("Subsystem 1 Initial State:")
        SUB1.print_waiting_queue()
        print("\nSubsystem 3 Initial State:")  # Uncomment this
        print(f"Real-time tasks to schedule: {len(sub3_tasks)}")  # Uncomment this
        print("\nSubsystem 4 Initial State:")
        print(f"Tasks to schedule with prerequisites: {len(sub4_tasks)}")
        
        input('Press Enter to start...')
        print('---------------------------------------------')
        
        subsystem1_thread = threading.Thread(target=SUB1.start_subsystem, args=())
        subsystem2_thread = threading.Thread(target=SUB2.start_subsystem, args=())
        subsystem3_thread = threading.Thread(target=SUB3.start_subsystem)  # Uncomment this
        subsystem4_thread = threading.Thread(target=SUB4.start_subsystem)

        subsystems_threads.extend([subsystem1_thread, subsystem2_thread, subsystem3_thread, subsystem4_thread])  # Add subsystem3_thread
        
        Time = 0
        for sub_thread in subsystems_threads:
            sub_thread.start()
        
        while True:
            print(f'\n{"="*100}')
            print('Time: ', Time)
            print('during processing')
            # Reset quantum status tracking
            SUB1.quantum_tasks = {
                'core1': None,
                'core2': None,  
                'core3': None
            }
            # SUB3.quantum_task = None
            
            SUB1.set_clock()
            SUB2.set_clock()
            SUB3.set_clock()  # Uncomment this
            SUB4.set_clock()
            
            while True:
                if (SUB1.is_processores_finished() and 
                    SUB2.is_processores_finished() and
                    SUB3.is_processor_finished() and
                    SUB4.is_processores_finished()):
                    break
                # time.sleep(0.1)
            print(f'\n{"-"*50}')
            print('after all subsystems finished')
            print('SUB1: ')
            print(f'\tResources: R1: {SUB1.reamining_resource1_number}/{sub1_r1}, R2: {SUB1.reamining_resource2_number}/{sub1_r2}')
            
            # print('\tProcessing Status:')
            # for core_num, (current_task, busy_time, quantum_task) in enumerate([
            #     (SUB1.processor1_assigned_task, SUB1.processor1_busy_time, SUB1.quantum_tasks['core1']),
            #     (SUB1.processor2_assigned_task, SUB1.processor2_busy_time, SUB1.quantum_tasks['core2']),
            #     (SUB1.processor3_assigned_task, SUB1.processor3_busy_time, SUB1.quantum_tasks['core3'])
            # ], 1):
            #     if quantum_task:
            #         status = 'Running' if current_task else 'Completed'
            #         print(f'\t\tCore {core_num}: Task {quantum_task.name} - {status} (Busy time: {busy_time})')
            #     else:
            #         print(f'\t\tCore {core_num}: No task processed (Busy time: {busy_time})')
            
            print('\tWhat Cores did')
            for core in SUB1.subsystem_did:
                print(f'\t\t{core} did :{SUB1.subsystem_did[core]}')
            
            # Show waiting queue status
            print('\tWaiting Queue:')
            if not SUB1.Waiting_queue.empty():
                for _, task in list(SUB1.Waiting_queue.queue):
                    print(f'\t\t{task} - Arrival: {task.arrival_time}')
            else:
                print('\t\tEmpty')

            # Show ready queues status
            print('\tReady Queues:')
            for queue_num, queue in enumerate([SUB1.Ready_queue1, SUB1.Ready_queue2, SUB1.Ready_queue3], 1):
                print(f'\t\tQueue {queue_num}: {[task.name for task in queue] if queue else "Empty"}')
                
            print(f'\tFinished Tasks: {[task.name for task in SUB1.finished_tasks]}')
            
        
            print('\nSUB2:')
            print(f'\tResources: R1: {SUB2.reamining_resource1_number}/{sub2_r1}, R2: {SUB2.reamining_resource2_number}/{sub2_r2}')
            
            print('\tProcessing Status:')
            for core_num, (current_task, busy_time) in enumerate([
                (SUB2.processor1_assigned_task, SUB2.processor1_busy_time),
                (SUB2.processor2_assigned_task, SUB2.processor2_busy_time)
            ], 1):
                if current_task:
                    print(f'\t\tCore {core_num}: Task {current_task.name} - Running (Busy time: {busy_time})')
                else:
                    print(f'\t\tCore {core_num}: No task processed (Busy time: {busy_time})')

            # Show ready queue status
            print('\tReady Queue:')
            if not SUB2.Ready_queue.empty():
                ready_tasks = list(SUB2.Ready_queue.queue)
                print(f'\t\tTasks: {[task[1].name for task in ready_tasks]}')
            else:
                print('\t\tEmpty')
                
            print(f'\tFinished/Aborted Tasks: {[task.name for task in SUB2.finished_and_aborted_tasks]}')

            # Print Subsystem 3 status
            print('\nSUB3 (Real-time):')
            status_line = None
            
            if SUB3.just_completed and SUB3.processor_busy_time == 0:
                # Show BURST FINISHED status for the quantum where task completes
                status_line = f'\tTask {SUB3.just_completed.name} - Processing (Busy time: 0, BURST FINISHED)'
                SUB3.just_completed = None  # Clear it after showing
                SUB3.quantum_task = None  # Also clear quantum_task
            elif SUB3.processor_assigned_task:
                task = SUB3.processor_assigned_task
                accept_status = "Accepted" if task.is_accepted else "Rejected" if task.is_accepted is not None else "Pending"
                status = f"Running (Busy time: {SUB3.processor_busy_time}, {accept_status}, speedup: {task.speedup_needed})"
                status_line = f'\tTask {task.name} - {status}'
            else:
                status_line = '\tNo tasks available' if len(SUB3.Ready_queue) == 0 and len(SUB3.waiting_arrivals) == 0 else f'\tWaiting for next task (Busy time: {SUB3.processor_busy_time})'
            print(status_line)

            print('\tWaiting Arrivals:')
            for task in SUB3.waiting_arrivals:
                status = "BURST FINISHED" if task.current_burst_complete else "Accepted" if task.is_accepted else "Rejected" if task.is_accepted is not None else "Pending"
                print(f'\t\t{task.name} ({status})')
                
            print('\tReady Queue:')
            for task in SUB3.Ready_queue:
                status = "BURST FINISHED" if task.current_burst_complete else "Accepted" if task.is_accepted else "Rejected" if task.is_accepted is not None else "Pending"
                print(f'\t\t{task.name} ({status})')
                
            print(f'\tCompleted Periods: {SUB3.completed_periods}')
            print(f'\tFinished Tasks: {[task.name for task in SUB3.finished_tasks]}')
            print(f'\tRejected Tasks: {[task.name for task in SUB3.rejected_tasks]}')

            # Add SUB4 status display
            print('\nSUB4:')
            print(f'\tResources: R1: {SUB4.reamining_resource1_number}/{sub4_r1}, R2: {SUB4.reamining_resource2_number}/{sub4_r2}')
            
            print('\tWhat Cores did')
            for core in SUB4.subsystem_did:
                print(f'\t\t{core} did: {SUB4.subsystem_did[core]}')
            
            print('\tWaiting Queue:', len(SUB4.Waiting_queue))
            print('\tReady Queue:', len(SUB4.Ready_queue))
            print(f'\tFinished Tasks: {[task.name for task in SUB4.finished_tasks if task]}')

            # Update completion check
            if (len(SUB1.finished_tasks) == len(sub1_tasks) and
                len(SUB2.finished_and_aborted_tasks) == len(sub2_tasks) and
                len(SUB3.finished_tasks) + len(SUB3.rejected_tasks) == len(sub3_tasks) and
                len([t for t in SUB4.finished_tasks if t]) == len(sub4_tasks)):
                print("\nAll tasks completed successfully!")
                self.execution_tracker.save_report()
                break
            
            Time += 1
        
        for sub_thread in subsystems_threads:
            sub_thread.join()
        
        # ----------------------------------------------------------------------------------
        '''
        These codes are not complete
        '''
        # sub2_tasks = []
        # for task in sub2_tasks_dict:
        #     temp_task = subsystem2_task(task['name'], task['execution_time'],
        #                                 task['resource1_usage'], task['resource2_usage'],
        #                                 task['arrival_time'], task['processor_number'])
        #     sub2_tasks.append(temp_task)
        
        # sub3_tasks = []
        # for task in sub3_tasks_dict:
        #     temp_task = subsystem3_task(task['name'], task['execution_time'],
        #                                 task['resource1_usage'], task['resource2_usage'],
        #                                 task['arrival_time'], task['processor_number'])
        #     sub3_tasks.append(temp_task)
        
        # ----------------------------------------------------------------------------------


