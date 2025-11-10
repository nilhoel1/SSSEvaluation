import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import math
from SimpleTests_ct import SparseWorkloadFunction_CT
from care_taking_task import find_largest_sparse_T

def test_schedulable():
    tasks = [
        {'name': 'T1', 'execution': 1, 'period': 3, 'deadline': 3},
        {'name': 'T2', 'execution': 2, 'period': 8, 'deadline': 8},
    ]
    ct_tasks = [
        {'name': 'CT1', 'execution': 1},
        {'name': 'CT2', 'execution': 3},
    ]
    T_sparse = 10
    assert SparseWorkloadFunction_CT(tasks, ct_tasks, T_sparse)

def test_unschedulable():
    tasks = [
        {'name': 'T1', 'execution': 2, 'period': 4, 'deadline': 4},
        {'name': 'T2', 'execution': 3, 'period': 5, 'deadline': 5},
    ]
    ct_tasks = [
        {'name': 'CT1', 'execution': 1},
        {'name': 'CT2', 'execution': 1},
    ]
    T_sparse = 2
    assert not SparseWorkloadFunction_CT(tasks, ct_tasks, T_sparse)

def test_find_T_simple():
    """ Test case where a valid hat_T should be found. """
    ct_tasks = [
        {'execution': 1, 'Delta_down': 10, 'Delta_up': 20},
    ]
    assert find_largest_sparse_T(ct_tasks) == 20

def test_no_T_found():
    """ Test case where no valid hat_T should be found. """
    ct_tasks = [
        {'execution': 1, 'Delta_down': 1, 'Delta_up': 1},
        {'execution': 1, 'Delta_down': 1, 'Delta_up': 1},
    ]
    assert find_largest_sparse_T(ct_tasks) is None

def test_empty_tasks():
    """ Test with an empty list of tasks. """
    ct_tasks = []
    assert find_largest_sparse_T(ct_tasks) is None

def test_find_T_two_tasks():
    """ A more complex case with two tasks. """
    ct_tasks = [
        {'execution': 1, 'Delta_down': 10, 'Delta_up': 100},
        {'execution': 1, 'Delta_down': 50, 'Delta_up': 100},
    ]
    assert find_largest_sparse_T(ct_tasks) == 49

def test_find_T_complex_two_tasks():
    """ A more complex case with two tasks with different omega sizes. """
    ct_tasks = [
        {'execution': 1, 'Delta_down': 10, 'Delta_up': 100},
        {'execution': 1, 'Delta_down': 40, 'Delta_up': 100},
    ]
    assert find_largest_sparse_T(ct_tasks) == 39

def test_find_T_complex_two_tasks_2():
    """ Test case with two tasks that results in a smaller hat_T. """
    ct_tasks = [
        {'execution': 1, 'Delta_down': 10, 'Delta_up': 19},
        {'execution': 1, 'Delta_down': 10, 'Delta_up': 100},
    ]
    assert find_largest_sparse_T(ct_tasks) == 9

def test_find_T_three_tasks():
    """ A more complex case with three tasks. """
    ct_tasks = [
        {'execution': 1, 'Delta_down': 10, 'Delta_up': 100},
        {'execution': 1, 'Delta_down': 20, 'Delta_up': 100},
        {'execution': 1, 'Delta_down': 30, 'Delta_up': 100},
    ]
    assert find_largest_sparse_T(ct_tasks) == 14
