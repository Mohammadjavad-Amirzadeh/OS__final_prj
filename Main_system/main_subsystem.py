import threading
from Main_system.get_input import get_input
from SubSystems.subsystem1.subsystem1_task import subsystem1_task
from SubSystems.subsystem1.subsystem1_main import subsystem1
from SubSystems.subsystem3.subsystem3_task import subsystem3_task
from SubSystems.subsystem3.subsystem3_main import subsystem3
from SubSystems.subsystem2.subsystem2_task import subsystem2_task
from SubSystems.subsystem2.subsystem2_main import subsystem2
import time

def get_available_resources():
    # Temporary implementation - will be expanded later
    return 0, 0

def request_resources(r1_needed, r2_needed):
    # Temporary implementation - will be expanded later
    return 0, 0

def run():
    subsystems_threads = []
    sub1_tasks_dict, sub2_tasks_dict, sub3_tasks_dict, sub1_r1, sub1_r2, sub2_r1, sub2_r2, sub3_r1, sub3_r2 = get_input()
    
    # Initialize subsystem 1
    sub1_tasks = []
    for task in sub1_tasks_dict:
        temp_task = subsystem1_task(task['name'], task['execution_time'],
                                  task['resource1_usage'], task['resource2_usage'],
                                  task['arrival_time'], task['processor_number'])
        sub1_tasks.append(temp_task)
    
    # Initialize subsystem 2
    # sub2_tasks = []
    # for task in sub2_tasks_dict:
    #     temp_task = subsystem2_task(task['name'], task['execution_time'],
    #                               task['resource1_usage'], task['resource2_usage'],
    #                               task['arrival_time'])
    #     sub2_tasks.append(temp_task)
    
    # # Initialize subsystem 3
    # sub3_tasks = []
    # for task in sub3_tasks_dict:
    #     temp_task = subsystem3_task(task['name'], task['execution_time'],
    #                               task['resource1_usage'], task['resource2_usage'],
    #                               task['arrival_time'], task['period'],
    #                               task['repetitions_number'])
    #     sub3_tasks.append(temp_task)
    
    SUB1 = subsystem1(sub1_tasks, sub1_r1, sub1_r2)
    # SUB2 = subsystem2(sub2_tasks, sub2_r1, sub2_r2)
    # SUB3 = subsystem3(sub3_tasks)
    
    print("Subsystem 1 Initial State:")
    SUB1.print_waiting_queue()
    # print("\nSubsystem 3 Initial State:")
    # print(f"Real-time tasks to schedule: {len(sub3_tasks)}")
    
    input('Press Enter to start...')
    print('---------------------------------------------')
    
    subsystem1_thread = threading.Thread(target=SUB1.start_subsystem, args=())
    # subsystem2_thread = threading.Thread(target=SUB2.start_subsystem, args=())
    # subsystem3_thread = threading.Thread(target=SUB3.start_subsystem, args=())
    
    subsystems_threads.extend([subsystem1_thread])
    
    Time = 0
    for sub_thread in subsystems_threads:
        sub_thread.start()
    
    while True:
        print(f'\n{"="*50}')
        print('Time: ', Time)
        
        # Reset quantum status tracking
        SUB1.quantum_tasks = {
            'core1': None,
            'core2': None,  
            'core3': None
        }
        # SUB3.quantum_task = None
        
        SUB1.set_clock()
        # SUB2.set_clock()
        # SUB3.set_clock()
        
        while True:
            if (SUB1.is_processores_finished()):
                break
            time.sleep(0.1)
            
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
        
        # Print Subsystem 2 status
        # print('\nSUB2:')
        # print(f'\tResources: R1: {SUB2.reamining_resource1_number}/{sub2_r1}, R2: {SUB2.reamining_resource2_number}/{sub2_r2}')
        
        # print('\tProcessing Status:')
        # for core_num, (current_task, busy_time) in enumerate([
        #     (SUB2.processor1_assigned_task, SUB2.processor1_busy_time),
        #     (SUB2.processor2_assigned_task, SUB2.processor2_busy_time)
        # ], 1):
        #     if current_task:
        #         print(f'\t\tCore {core_num}: Task {current_task.name} - Running (Busy time: {busy_time})')
        #     else:
        #         print(f'\t\tCore {core_num}: No task processed (Busy time: {busy_time})')

        # # Show ready queue status
        # print('\tReady Queue:')
        # if not SUB2.Ready_queue.empty():
        #     ready_tasks = list(SUB2.Ready_queue.queue)
        #     print(f'\t\tTasks: {[task[1].name for task in ready_tasks]}')
        # else:
        #     print('\t\tEmpty')
            
        # print(f'\tFinished/Aborted Tasks: {[task.name for task in SUB2.finished_and_aborted_tasks]}')

        # Print Subsystem 3 status
        # print('\nSUB3 (Real-time):')
        # status_line = None
        # if SUB3.processor_assigned_task:
        #     if SUB3.processor_busy_time > 0:
        #         status_line = f'\tTask {SUB3.processor_assigned_task.name} - Running (Busy time: {SUB3.processor_busy_time})'
        #     else:
        #         status_line = f'\tTask {SUB3.processor_assigned_task.name} - Completed (Busy time: {SUB3.processor_busy_time})'
        # elif SUB3.quantum_task:
        #     status_line = f'\tTask {SUB3.quantum_task.name} - Processing (Busy time: {SUB3.processor_busy_time})'
        # else:
        #     if len(SUB3.Ready_queue) == 0 and len(SUB3.waiting_arrivals) == 0:
        #         status_line = f'\tNo tasks available'
        #     else:
        #         status_line = f'\tWaiting for next task (Busy time: {SUB3.processor_busy_time})'
        # print(status_line)

        # print(f'\tWaiting Arrivals: {[task.name for task in SUB3.waiting_arrivals]}')
        # print(f'\tReady Queue: {[task.name for task in SUB3.Ready_queue]}')
        # if SUB3.missed_deadlines > 0:
        #     print(f'\tMissed Deadlines: {SUB3.missed_deadlines}')
        # print(f'\tCompleted Periods: {SUB3.completed_periods}')
        
        if (len(SUB1.finished_tasks) == len(sub1_tasks) 
            # len(SUB2.finished_and_aborted_tasks) == len(sub2_tasks)
            # all(task.repetitions_number <= 0 for task in SUB3.Ready_queue)
            ):
            print("\nAll tasks completed successfully!")
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