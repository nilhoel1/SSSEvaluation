import math

# Liu and Layland bound
# Input: Task set
# Output: Schedulability of task set
def LiuAndLaylandBound_CT(tasks, ct_tasks):
    utilization = 0
    for task, ct_task in zip(tasks, ct_tasks):
        utilization += task['execution'] / task['period']
        utilization += ct_task['execution'] / task['period']

    bound = len(tasks) * (2**(1/len(tasks)) - 1)

    return utilization <= bound

# Hyperbolic bound
# Input: Task set
# Output: Schedulability of task set
def HyperbolicBound_CT(tasks, ct_tasks):
    product = 1
    for task, ct_task in zip(tasks, ct_tasks):
        product *= ((task['execution'] + ct_task['execution'])/ task['period']) + 1

    return product <= 2

# Time Demand Analysis
# Input: Task set
# Output: Schedulability of task set
def TimeDemandAnalysis_CT(tasks, ct_tasks):
    # Assunme: tasks and ct_tasks are sorted by priority
    for idx in range(len(tasks)):
        wcrt = TimeDemandAnalysis_WCRT(tasks[idx], ct_tasks[idx], tasks[:idx], ct_tasks[:idx])
        if wcrt > tasks[idx]['deadline']:  # deadline miss
            return False
        else:
            tasks[idx]['wcrt'] = wcrt  # set wcrt
            continue
    return True

# Compute the response time bound for TDA.
# Input: Task, higher priority tasks
# Output: Worst-case response time of task
def TimeDemandAnalysis_WCRT(task, ct_task, HPTasks, ct_HPTasks):
    t = task['execution'] + ct_task['execution']
    while True:
        wcrt = task['execution']
        for itask, ct_itask in zip(HPTasks, ct_HPTasks):
            wcrt += math.ceil(t / itask['period']) * itask['execution'] + math.ceil(t / ct_itask['period']) * ct_itask['execution']

        if (wcrt > task['deadline'] or wcrt <= t):
            break
        t = wcrt
    return wcrt

# Sparse Workload Function
# Input: Task set, care-taking task set, sparse interval T
# Output: Schedulability of task set
def SparseWorkloadFunction_CT(tasks, ct_tasks_sparse, ct_tasks):
    T_sparse = ct_tasks_sparse[0]['period']

    # Assume tasks are sorted by priority (Rate Monotonic)
    for i in range(len(tasks)):
        task_i = tasks[i]
        hp_tasks = tasks[:i]
        hp_ct_tasks = ct_tasks[:i]

        if not hp_ct_tasks:
            c_max_k = 0
        else:
            c_max_k = max(ct_task['execution'] for ct_task in hp_ct_tasks)

        # Iterative calculation to find the response time
        t = task_i['execution'] + c_max_k
        while True:
            workload = task_i['execution'] + c_max_k
            for hp_task in hp_tasks:
                workload += math.ceil(t / hp_task['period']) * hp_task['execution']

            if workload == t:
                wcrt = workload
                break
            if workload > task_i['deadline']:
                return False  # Deadline miss

            t = workload

        if wcrt > task_i['deadline']:
            return False

    return True
