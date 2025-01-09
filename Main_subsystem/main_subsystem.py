from Main_subsystem.get_input import get_input
from SubSystems.subsystem1.subsystem1_task import subsystem1_task

def run():
    sub1_tasks_dict, sub2_tasks_dict, sub3_tasks_dict = get_input()
    sub1_tasks = []
    for task in sub1_tasks_dict:
        temp_task = subsystem1_task(task['name'], task['execution_time'], \
                                    task['resource1_usage'], task['resource2_usage'], \
                                    task['arrival_time'], task['processor_number'])
        sub1_tasks.append(temp_task)
        
    print(sub1_tasks)
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