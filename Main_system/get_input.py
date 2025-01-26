import json
from datetime import datetime

def log_rejected_task(task_name, subsystem, reason):
    try:
        with open('rejected_tasks.json', 'r') as f:
            log = json.load(f)
    except FileNotFoundError:
        log = []

    log.append({
        'task_name': task_name,
        'subsystem': subsystem,
        'reason': reason,
        'timestamp': datetime.now().isoformat()
    })

    with open('rejected_tasks.json', 'w') as f:
        json.dump(log, f, indent=4)

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
            if task_dict['resource1_usage'] > sub1_r1 or task_dict['resource2_usage'] > sub1_r2:
                log_rejected_task(task_dict['name'], 'Sub System1', 'Resource requirement exceeds available resources')
                print(f"Task {task_dict['name']} rejected: Resource requirement exceeds available resources")
            else:
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
            if task_dict['resource1_usage'] > sub2_r1 or task_dict['resource2_usage'] > sub2_r2:
                log_rejected_task(task_dict['name'], 'Sub System2', 'Resource requirement exceeds available resources')
                print(f"Task {task_dict['name']} rejected: Resource requirement exceeds available resources")
            else:
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
            task_dict = {
                'name': name,
                'execution_time': int(exec_time),
                'resource1_usage': int(r1_usage),
                'resource2_usage': int(r2_usage),
                'arrival_time': int(arrival),
                'period': int(period),
                'repetitions_number': int(reps)
            }
            if task_dict['resource1_usage'] > sub3_r1 or task_dict['resource2_usage'] > sub3_r2:
                log_rejected_task(task_dict['name'], 'Sub System3', 'Resource requirement exceeds available resources')
                print(f"Task {task_dict['name']} rejected: Resource requirement exceeds available resources")
            else:
                sub3_tasks.append(task_dict)
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
    rejected_tasks = set()  # Track rejected task names
    tasks_to_process = []   # Store tasks temporarily to check dependencies

    # First pass - collect all tasks and do resource validation
    while True:
        line = input()
        if line == '$':
            break
        name, exec_time, r1, r2, arrival, prerequisite = line.split()
        if prerequisite == "-":
            prerequisite = None
        task_dict = {
            'name': name,
            'execution_time': int(exec_time),
            'resource1_usage': int(r1),
            'resource2_usage': int(r2),
            'arrival_time': int(arrival),
            'prerequisite_task': prerequisite
        }
        
        # First check resources
        if task_dict['resource1_usage'] > sub4_r1 or task_dict['resource2_usage'] > sub4_r2:
            log_rejected_task(task_dict['name'], 'Sub System4', 'Resource requirement exceeds available resources')
            print(f"Task {task_dict['name']} rejected: Resource requirement exceeds available resources")
            rejected_tasks.add(task_dict['name'])
        else:
            tasks_to_process.append(task_dict)

    # Second pass - check dependencies
    while tasks_to_process:
        tasks_added = []
        tasks_rejected = []
        
        for task in tasks_to_process:
            if task['prerequisite_task'] is None:
                # No dependencies, can be added
                sub4_tasks.append(task)
                tasks_added.append(task)
            elif task['prerequisite_task'] in rejected_tasks:
                # Prerequisite was rejected, reject this task too
                log_rejected_task(task['name'], 'Sub System4', 
                                f"Prerequisite task {task['prerequisite_task']} was rejected")
                print(f"Task {task['name']} rejected: Prerequisite task {task['prerequisite_task']} was rejected")
                rejected_tasks.add(task['name'])
                tasks_rejected.append(task)
            elif any(t['name'] == task['prerequisite_task'] for t in sub4_tasks):
                # Prerequisite exists in accepted tasks
                sub4_tasks.append(task)
                tasks_added.append(task)
            
        # Remove processed tasks
        for task in tasks_added + tasks_rejected:
            tasks_to_process.remove(task)
            
        # If no tasks were processed in this iteration but tasks remain,
        # they have invalid dependencies
        if not (tasks_added or tasks_rejected) and tasks_to_process:
            for task in tasks_to_process:
                log_rejected_task(task['name'], 'Sub System4', 
                                f"Invalid or circular prerequisite dependency: {task['prerequisite_task']}")
                print(f"Task {task['name']} rejected: Invalid or circular prerequisite dependency")
            break

    return (sub1_tasks, sub2_tasks, sub3_tasks, sub4_tasks, 
            sub1_r1, sub1_r2, sub2_r1, sub2_r2, sub3_r1, sub3_r2, sub4_r1, sub4_r2)
