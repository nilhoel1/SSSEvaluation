
import random
import math

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
            'execution': task['execution'] * wcet_bound_ratio,
            'Delta_down': task['period'] * delta_down_multiplier,
            'Delta_up': task['period'] * delta_up_multiplier,
        }
        care_taking_tasks.append(care_taking_task)
    return care_taking_tasks

def ct_to_rt_simple(real_time_tasks, care_taking_tasks):
    """
    Merges real-time and care-taking tasks based on Lemma 6 from main.pdf.
    Each care-taking task is replaced by a sporadic real-time task with period Delta_down.
    """
    tasks = list()
    for ct_task, rt_task in zip(care_taking_tasks, real_time_tasks):
        new_task = {
            'period': ct_task['Delta_down'],
            'execution': ct_task['execution'],
            # No deadline for cat_tasks, so making it infinity
            'deadline': float('inf'),
            'utilization': ct_task['execution'] / ct_task['Delta_down'],
            'sslength': 0,
            # 'paths': [],
            # 'Cseg': [],
            # 'Sseg': []
        }
        tasks.append(new_task)
    return tasks

def ct_to_rt_sparse(real_time_tasks, care_taking_tasks, T):
    """
    Merges real-time and care-taking tasks based on Lemma 15 from main.pdf.
    This is a simplified interpretation for a whole system analysis.
    All care-taking tasks are replaced by a single sporadic task with WCET equal to the max WCET of all care-taking tasks.
    """
    merged_tasks = list(real_time_tasks)

    if care_taking_tasks:
        execution_max = max(ct['execution'] for ct in care_taking_tasks)
        blocking_task = {
            'period': T,
            'execution': execution_max,
            'deadline': T,  # Assuming implicit deadline
            'utilization': execution_max / T,
            'sslength': 0,
            # 'paths': [],
            # 'Cseg': [],
            # 'Sseg': []
        }
        merged_tasks.append(blocking_task)

    return merged_tasks

def theorem_13_test(ct_tasks, hat_T):
    """
    Checks the condition from Theorem 13 in main.pdf for a set of care-taking tasks.

    Args:
        ct_tasks: A list of care-taking task dictionaries.
        hat_T: The given hat_T parameter.

    Returns:
        True if the condition holds for all tasks, False otherwise.
    """
    omega_sizes = [math.floor(task['Delta_up'] / hat_T) - math.ceil(task['Delta_down'] / hat_T) + 1 for task in ct_tasks]

    for i, task_i in enumerate(ct_tasks):
        omega_i_size = omega_sizes[i]

        # Determine L_i
        L_i = []
        for l, ct_task_l in enumerate(ct_tasks):
            omega_l_size = omega_sizes[l]
            if omega_l_size < omega_i_size:
                L_i.append(ct_task_l)
            elif omega_l_size == omega_i_size and l < i:
                L_i.append(ct_task_l)

        # Check the condition for at least one t in {1, ..., |Omega_i|}
        condition_holds_for_i = False
        if omega_i_size < 1:
            return False

        for t in range(1, int(omega_i_size) + 1):
            sum_val = 0
            for ct_task_l in L_i:
                denominator = max(math.ceil(ct_task_l['Delta_down'] / hat_T), 1)
                if denominator > 0:
                    sum_val += math.floor(t / denominator)

            if 1 + sum_val < t:
                condition_holds_for_i = True
                break

        if not condition_holds_for_i:
            return False

    return True

def find_smallest_sparse_T(ct_tasks):
    """
    Finds the smallest hat_T for which the theorem_13_test passes.

    Args:
        ct_tasks: A list of care-taking task dictionaries.

    Returns:
        The smallest hat_T found, or None if no such hat_T is found.
    """
    if not ct_tasks:
        return None

    start_T = 1 # = max(task['Delta_down'] for task in ct_tasks)
    max_T = min(task['Delta_up'] for task in ct_tasks)
    for hat_T in range(int(max_T), int(start_T) - 1, -1):
        if theorem_13_test(ct_tasks, hat_T):
            return hat_T

    return None
