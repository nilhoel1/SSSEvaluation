
import unittest
import math
from care_taking_task import theorem_13_test, find_smallest_sparse_T, ct_to_rt_simple, ct_to_rt_sparse

class TestCareTaking(unittest.TestCase):

    def test_theorem_13_simple_pass(self):
        ct_tasks = [{'Delta_down': 100, 'Delta_up': 200, 'execution': 1}]
        hat_T = 10
        self.assertTrue(theorem_13_test(ct_tasks, hat_T))

    def test_theorem_13_simple_fail(self):
        ct_tasks = [{'Delta_down': 100, 'Delta_up': 105, 'execution': 1}]
        hat_T = 10
        self.assertFalse(theorem_13_test(ct_tasks, hat_T))

    def test_theorem_13_multiple_tasks_pass(self):
        ct_tasks = [
            {'Delta_down': 100, 'Delta_up': 200, 'execution': 1},
            {'Delta_down': 120, 'Delta_up': 180, 'execution': 1}
        ]
        hat_T = 10
        self.assertTrue(theorem_13_test(ct_tasks, hat_T))

    def test_find_smallest_sparse_T_found(self):
        ct_tasks = [{'Delta_down': 100, 'Delta_up': 200, 'execution': 1}]
        self.assertEqual(find_smallest_sparse_T(ct_tasks), 100)

    def test_find_smallest_sparse_T_not_found(self):
        ct_tasks = [{'Delta_down': 100, 'Delta_up': 101, 'execution': 1}]
        self.assertIsNone(find_smallest_sparse_T(ct_tasks))

    def test_find_smallest_sparse_T_empty_tasks(self):
        ct_tasks = []
        self.assertIsNone(find_smallest_sparse_T(ct_tasks))

    def test_ct_to_rt_simple(self):
        rt_tasks = [{'period': 100, 'execution': 10}]
        ct_tasks = [{'Delta_down': 50, 'execution': 5}]
        expected = [{
            'period': 50,
            'execution': 5,
            'deadline': float('inf'),
            'utilization': 0.1,
            'sslength': 0
        }]
        self.assertEqual(ct_to_rt_simple(rt_tasks, ct_tasks), expected)

    def test_ct_to_rt_sparse(self):
        rt_tasks = [{'period': 100, 'execution': 10}]
        ct_tasks = [{'execution': 5}, {'execution': 8}]
        T = 1000
        merged_tasks = ct_to_rt_sparse(rt_tasks, ct_tasks, T)
        self.assertEqual(len(merged_tasks), 2)
        self.assertEqual(merged_tasks[1]['execution'], 8)
        self.assertEqual(merged_tasks[1]['period'], T)

    def test_theorem_13_non_empty_L_pass(self):
        ct_tasks = [
            {'Delta_down': 100, 'Delta_up': 150, 'execution': 1},
            {'Delta_down': 100, 'Delta_up': 200, 'execution': 1}
        ]
        hat_T = 10
        self.assertTrue(theorem_13_test(ct_tasks, hat_T))

if __name__ == '__main__':
    unittest.main()
