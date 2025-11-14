#!/bin/bash

# row1
./.venv/bin/python3 run_careTaking.py --plot_sets --NumberOfTasksPerSet 5 --ct_wcet_mul 0.5 --ct_d_down_mult 5 --ct_d_up_mult 10 &

./.venv/bin/python3 run_careTaking.py --plot_sets --NumberOfTasksPerSet 5 --ct_wcet_mul 0.5 --ct_d_down_mult 50 --ct_d_up_mult 100 &

./.venv/bin/python3 run_careTaking.py --plot_sets --NumberOfTasksPerSet 2 --ct_wcet_mul 0.5 --ct_d_down_mult 100 --ct_d_up_mult 200 &

# row2
./.venv/bin/python3 run_careTaking.py --plot_sets --NumberOfTasksPerSet 10 --ct_wcet_mul 1 --ct_d_down_mult 5 --ct_d_up_mult 10 &

./.venv/bin/python3 run_careTaking.py --plot_sets --NumberOfTasksPerSet 10 --ct_wcet_mul 1 --ct_d_down_mult 50 --ct_d_up_mult 100 &

./.venv/bin/python3 run_careTaking.py --plot_sets --NumberOfTasksPerSet 10 --ct_wcet_mul 1 --ct_d_down_mult 100 --ct_d_up_mult 200 &

# row3
./.venv/bin/python3 run_careTaking.py --plot_sets --NumberOfTasksPerSet 50 --ct_wcet_mul 1.5 --ct_d_down_mult 5 --ct_d_up_mult 10 &

./.venv/bin/python3 run_careTaking.py --plot_sets --NumberOfTasksPerSet 50 --ct_wcet_mul 1.5 --ct_d_down_mult 50 --ct_d_up_mult 100 &

./.venv/bin/python3 run_careTaking.py --plot_sets --NumberOfTasksPerSet 50 --ct_wcet_mul 5 --ct_d_down_mult 100 --ct_d_up_mult 200 &

# Wait for all background processes to complete
wait
