def get_input():
    sub1_r1, sub1_r2 = map(int, input().split())
    sub2_r1, sub2_r2 = map(int, input().split())
    sub3_r1, sub3_r2 = map(int, input().split())
    print()
    print('-----------------------------------')
    print('Enter Sub System1 Tasks')
    sub1_tasks = []
    while True:
        temp = input()
        if temp == '$':
            break
        else:
            task = temp.split()
            task_dict = {
                'name': task[0],
                'execution_time': int(task[1]),
                'resource1_usage': int(task[2]),
                'resource2_usage': int(task[3]),
                'arrival_time': int(task[4]), 
                'processor_number': int(task[5])
            }
            sub1_tasks.append(task_dict)
    # print(f'SUB SYSTEM 1 TASKS : {sub1_tasks}')
    print()
    
    
    print('-----------------------------------')
    print('Enter Sub System2 Tasks')
    sub2_tasks = []
    while True:
        temp = input()
        if temp == '$':
            break
        else:
            task = temp.split()
            task_dict = {
                'name': task[0],
                'execution_time': int(task[1]),
                'resource1_usage': int(task[2]),
                'resource2_usage': int(task[3]),
                'arrival_time': int(task[4]), 
            }
            sub2_tasks.append(task_dict)
    # print(f'SUB SYSTEM 2 TASKS : {sub2_tasks}')
    print()
    
    
    print('-----------------------------------')
    print('Enter Sub System3 Tasks')
    sub3_tasks = []
    while True:
        temp = input()
        if temp == '$':
            break
        else:
            task = temp.split()
            task_dict = {
                'name': task[0],
                'execution_time': int(task[1]),
                'resource1_usage': int(task[2]),
                'resource2_usage': int(task[3]),
                'arrival_time': int(task[4]), 
                'period': int(task[5])
            }
            sub3_tasks.append(task_dict)
    # print(f'SUB SYSTEM 3 TASKS : {sub2_tasks}')
    print()
    
    
    return sub1_tasks, sub2_tasks, sub3_tasks, sub1_r1, sub1_r2, sub2_r1, sub2_r2, sub3_r1, sub3_r2
