
import random

def generate_care_taking_tasks(tasks, wcet_bound_ratio, delta_down_multiplier, delta_up_multiplier):
    """
    Generates care-taking tasks for a given set of real-time tasks.
    As defined in main.pdf, a care-taking task is (C^c, Delta_down, Delta_up).

    Args:
        tasks: A list of real-time task dictionaries.
        wcet_bound_ratio: The ratio of the real-time task's WCET for the care-taking task's WCET.
        delta_down_multiplier: Multiplier for the real-time task's period for Delta_down.
        delta_up_multiplier: Multiplier for the real-time task's period for Delta_up.

    Returns:
        A list of care-taking task dictionaries.
    """
    care_taking_tasks = []
    for task in tasks:
        care_taking_task = {
            'C^c': int(task['execution'] * wcet_bound_ratio),
            'Delta_down': int(task['period'] * delta_down_multiplier),
            'Delta_up': int(task['period'] * delta_up_multiplier),
            # Assuming priority is based on period if not present
            'priority': task.get('priority', task.get('period'))
        }
        care_taking_tasks.append(care_taking_task)
    return care_taking_tasks

def merge_tasks_simple(real_time_tasks, care_taking_tasks):
    """
    Merges real-time and care-taking tasks based on Lemma 6 from main.pdf.
    Each care-taking task is replaced by a sporadic real-time task with period Delta_down.
    """
    merged_tasks = list(real_time_tasks)
    for ct_task in care_taking_tasks:
        new_task = {
            'execution': ct_task['C^c'],
            'period': ct_task['Delta_down'],
            'deadline': ct_task['Delta_down'],  # Assuming implicit deadline
            'utilization': ct_task['C^c'] / ct_task['Delta_down'],
            'sslength': 0,
            'paths': [],
            'Cseg': [],
            'Sseg': []
        }
        merged_tasks.append(new_task)
    return merged_tasks

def merge_tasks_sparse(real_time_tasks, care_taking_tasks, T):
    """
    Merges real-time and care-taking tasks based on Lemma 15 from main.pdf.
    This is a simplified interpretation for a whole system analysis.
    All care-taking tasks are replaced by a single sporadic task with WCET equal to the max WCET of all care-taking tasks.
    """
    merged_tasks = list(real_time_tasks)

    if care_taking_tasks:
        c_max = max(ct['C^c'] for ct in care_taking_tasks)
        blocking_task = {
            'execution': c_max,
            'period': T,
            'deadline': T,  # Assuming implicit deadline
            'utilization': c_max / T,
            'sslength': 0,
            'paths': [],
            'Cseg': [],
            'Sseg': []
        }
        merged_tasks.append(blocking_task)

    return merged_tasks
