def get_input():
    sub1_r1, sub1_r2 = map(int, input().split())
    sub2_r1, sub2_r2 = map(int, input().split())
    sub3_r1, sub3_r2 = map(int, input().split())
    sub4_r1, sub4_r2 = map(int, input().split())
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
    print('Format: name execution_time r1_usage r2_usage arrival period repetitions')
    sub3_tasks = []
    while True:
        line = input()
        if line == '$':
            break
        try:
            name, exec_time, r1_usage, r2_usage, arrival, period, reps = line.split()
            sub3_tasks.append({
                'name': name,
                'execution_time': int(exec_time),
                'resource1_usage': int(r1_usage),
                'resource2_usage': int(r2_usage),
                'arrival_time': int(arrival),
                'period': int(period),
                'repetitions_number': int(reps)
            })
        except ValueError as e:
            print(f"Error: Invalid input format. Expected: name exec_time r1 r2 arrival period repetitions")
            print(f"Got: {line}")
            continue
    # print(f'SUB SYSTEM 3 TASKS : {sub2_tasks}')
    print()
    
    print('-----------------------------------')
    print('Enter Sub System4 Tasks')
    print("Format: name execution_time r1_usage r2_usage arrival prerequisite_task")
    sub4_tasks = []
    while True:
        line = input()
        if line == '$':
            break
        name, exec_time, r1, r2, arrival, prerequisite = line.split()
        if prerequisite == "-":
            prerequisite = None
        sub4_tasks.append({
            'name': name,
            'execution_time': int(exec_time),
            'resource1_usage': int(r1),
            'resource2_usage': int(r2),
            'arrival_time': int(arrival),
            'prerequisite_task': prerequisite
        })

    return (sub1_tasks, sub2_tasks, sub3_tasks, sub4_tasks, 
            sub1_r1, sub1_r2, sub2_r1, sub2_r2, sub3_r1, sub3_r2, sub4_r1, sub4_r2)
