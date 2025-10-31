import math

# Liu and Layland bound
# Input: Task set
# Output: Schedulability of task set
def LiuAndLaylandBound(tasks):
    utilization = 0
    for task in tasks:
        utilization += task['execution'] / task['period']
    
    bound = len(tasks) * (2**(1/len(tasks)) - 1)
    
    return utilization <= bound

# Hyperbolic bound
# Input: Task set
# Output: Schedulability of task set
def HyperbolicBound(tasks):
    product = 1
    for task in tasks:
        product *= (task['execution'] / task['period']) + 1
    
    return product <= 2

# Time Demand Analysis
# Input: Task set
# Output: Schedulability of task set
def TimeDemandAnalysis(tasks):
    for idx in range(len(tasks)):
        wcrt = TimeDemandAnalysis_WCRT(tasks[idx], tasks[:idx])
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
