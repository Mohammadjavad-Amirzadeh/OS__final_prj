import threading
from Main_system.get_input import get_input
from SubSystems.subsystem1.subsystem1_task import subsystem1_task
from SubSystems.subsystem1.subsystem1_main import subsystem1

import time

def run():
    subsystems_threads = []
    sub1_tasks_dict, sub2_tasks_dict, sub3_tasks_dict, sub1_r1, sub1_r2, sub2_r1, sub2_r2, sub3_r1, sub3_r2 = get_input()
    
    
    sub1_tasks = []
    for task in sub1_tasks_dict:
        temp_task = subsystem1_task(task['name'], task['execution_time'], \
                                    task['resource1_usage'], task['resource2_usage'], \
                                    task['arrival_time'], task['processor_number'])
        sub1_tasks.append(temp_task)
    
    SUB1 = subsystem1(sub1_tasks, sub1_r1, sub1_r2)
    SUB1.print_waiting_queue()
    # it has to go down after all sub systems initiated
    
    # SUB1.print_ready_queue1()
    # SUB1.print_ready_queue2()
    # SUB1.print_ready_queue3()
    # SUB1.print_waiting_queue()
    # SUB1.print_resources_list_status()
    input('enter')
    print('---------------------------------------------')
    # Fix: Remove the parentheses after start_subsystem
    subsystem1_thread = threading.Thread(target=SUB1.start_subsystem, args=())
    subsystems_threads.append(subsystem1_thread)
    
    
    Time = 0
    
    for sub_thread in subsystems_threads:
        sub_thread.start()
    
    while True:
        print(f'\n{"="*50}')
        print('Time: ', Time)
        SUB1.set_clock()
        
        while True:
            if SUB1.is_processores_finished():
                break
            time.sleep(0.1)
            
        print('SUB1: ')
        print(f'\tResources: R1: {SUB1.reamining_resource1_number}/{sub1_r1}, R2: {SUB1.reamining_resource2_number}/{sub1_r2}')
        
        # Add quantum completion status
        print('\tProcessing Status:')
        for core_num, (task, busy_time) in enumerate([
            (SUB1.processor1_assigned_task, SUB1.processor1_busy_time),
            (SUB1.processor2_assigned_task, SUB1.processor2_busy_time),
            (SUB1.processor3_assigned_task, SUB1.processor3_busy_time)
        ], 1):
            if task:
                status = "Running"
                if busy_time == 0:
                    if task.get_remaining_execution_time() <= 0:
                        status = "Completed"
                    else:
                        status = "Quantum Expired"
                print(f'\t\tCore {core_num}: {task} - {status} (Busy time: {busy_time})')
            else:
                print(f'\t\tCore {core_num}: Idle')

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
        
        if len(SUB1.finished_tasks) == len(sub1_tasks):
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
    #     temp_task = subsystem2_task(task['name'], task['execution_time'], \
    #                                 task['resource1_usage'], task['resource2_usage'], \
    #                                 task['arrival_time'], task['processor_number'])
    #     sub2_tasks.append(temp_task)
    
    # sub3_tasks = []
    # for task in sub3_tasks_dict:
    #     temp_task = subsystem3_task(task['name'], task['execution_time'], \
    #                                 task['resource1_usage'], task['resource2_usage'], \
    #                                 task['arrival_time'], task['processor_number'])
    #     sub3_tasks.append(temp_task)
    
    # ----------------------------------------------------------------------------------