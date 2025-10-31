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
        wcrt = TimeDemandAnalysis_WCRT(ct_tasks[idx], ct_tasks[:idx]) - ct_tasks[idx]['execution']
        wcrt += TimeDemandAnalysis_WCRT(tasks[idx], tasks[:idx])
        if wcrt > tasks[idx]['deadline']:  # deadline miss
            return False
        else:
            tasks[idx]['wcrt'] = wcrt  # set wcrt
            continue
    return True

# Compute the response time bound for TDA.
# Input: Task, higher priority tasks
# Output: Worst-case response time of task
def TimeDemandAnalysis_WCRT(task, HPTasks):
    t = task['execution']
    while True:
        wcrt = task['execution']
        for itask in HPTasks:
            wcrt += math.ceil(t / itask['period']) * itask['execution']

        if (wcrt > task['deadline'] or wcrt <= t):
            break
        t = wcrt
    return wcrt
