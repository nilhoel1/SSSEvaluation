import unittest
import math
from SimpleTests_ct import SparseWorkloadFunction_CT

class TestSparseWorkloadFunction(unittest.TestCase):

    def test_schedulable(self):
        tasks = [
            {'name': 'T1', 'execution': 1, 'period': 3, 'deadline': 3},
            {'name': 'T2', 'execution': 2, 'period': 8, 'deadline': 8},
        ]
        ct_tasks = [
            {'name': 'CT1', 'execution': 1},
            {'name': 'CT2', 'execution': 3},
        ]
        T_sparse = 10
        self.assertTrue(SparseWorkloadFunction_CT(tasks, ct_tasks, T_sparse))

    def test_unschedulable(self):
        tasks = [
            {'name': 'T1', 'execution': 2, 'period': 4, 'deadline': 4},
            {'name': 'T2', 'execution': 3, 'period': 5, 'deadline': 5},
        ]
        ct_tasks = [
            {'name': 'CT1', 'execution': 1},
            {'name': 'CT2', 'execution': 1},
        ]
        T_sparse = 2
        self.assertFalse(SparseWorkloadFunction_CT(tasks, ct_tasks, T_sparse))

if __name__ == '__main__':
    unittest.main()