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
    SUB1.set_clock()
    print('---------------------------------------------')
    subsystem1_thread = threading.Thread(target=SUB1.start_subsystem(), args=())
    subsystems_threads.append(subsystem1_thread)
    # for sub_thread in subsystems_threads:
    #     sub_thread.start()
    subsystem1_thread.start()
    
    for i in range(1000):
        print('yes')
        time.sleep(0.5)
        SUB1.set_clock()
    
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