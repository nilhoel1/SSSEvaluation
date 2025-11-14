import random
import argparse
import numpy as np
import copy
from schedTest.tgPath import taskGeneration_p
from schedTest.FixedPriority import SuspObl, SuspObl_WCRT
from careTaking.SimpleTests import LiuAndLaylandBound, HyperbolicBound, TimeDemandAnalysis
from careTaking.SimpleTests_ct import LiuAndLaylandBound_CT, HyperbolicBound_CT, TimeDemandAnalysis_CT, SparseWorkloadFunction_CT
from careTaking.plotting import plot_tasksets
from careTaking.care_taking_task import generate_care_taking_tasks, ct_to_rt_simple, ct_to_rt_sparse, find_largest_sparse_T, ct_to_rt_simple_opt
import time
import os
import shutil

def test_predefined_feasibility():
    """
    Tests the feasibility of a predefined set of care-taking tasks
    under the sparse model by finding the largest sparse period (hat_T).
    """
    # Task system as provided by the user.
    # Using C1 as execution time, T1 as Delta_down, and T2 as Delta_up.
    ct_tasks = [
        {'name': 'Prime', 'execution': 10, 'Delta_down': 1000, 'Delta_up': 2000},
        {'name': 'BinarySearch', 'execution': 10, 'Delta_down': 2500, 'Delta_up': 5000},
        {'name': 'PetriNet', 'execution': 10, 'Delta_down': 5000, 'Delta_up': 10000},
        {'name': 'InsertionSort', 'execution': 10, 'Delta_down': 50000, 'Delta_up': 100000},
    ]
    rt_tasks = [
        {'name': 'Prime', 'execution': 1, 'period': 20, 'deadline': 20},
        {'name': 'BinarySearch', 'execution': 8, 'period': 50, 'deadline': 50},
        {'name': 'PetriNet', 'execution': 28, 'period': 50, 'deadline': 50},
        {'name': 'InsertionSort', 'execution': 36, 'period': 1000, 'deadline': 1000},
    ]

    ct_rt_tasks = ct_to_rt_simple(rt_tasks, ct_tasks)

    print("Testing feasibility for the following care-taking tasks:")
    for task in ct_tasks:
        print(f"- {task['name']}: C={task['execution']}, Delta_down={task['Delta_down']}, Delta_up={task['Delta_up']}")
    print("-" * 30)

    # Find the largest sparse period T
    largest_T = find_largest_sparse_T(ct_tasks)
    feasible_sparse = SparseWorkloadFunction_CT(copy.deepcopy(rt_tasks), copy.deepcopy(ct_tasks), largest_T)
    feasible_naive = TimeDemandAnalysis_CT(copy.deepcopy(rt_tasks), copy.deepcopy(ct_rt_tasks))

    tda_res = TimeDemandAnalysis(copy.deepcopy(rt_tasks))


    if largest_T is not None:
        print(f"The largest sparse period (hat_T) found is: {largest_T}")
        if tda_res:
            print("RESULT: rt tasks Feasible.")
        else:
            print("RESULT: RT tasks are not fesible.")
        if feasible_sparse:
            print("RESULT: Feasible under the sparse model.")
        else:
            print("RESULT: NOT feasible under the sparse model.")
        if feasible_naive:
            print("RESULT: Feasible under the naive model.")
        else:
            print("RESULT: NOT feasible under the naive model.")
    else:
        print("RESULT: NOT feasible under the sparse model.")
        print("No suitable sparse period (hat_T) could be found.")

def main():
    """
    This script generates a task set using tgPath.py and checks its
    schedulability using various tests.
    """
    parser = argparse.ArgumentParser(description="Generate and test a task set.")
    parser.add_argument('--NumberOfTasksPerSet', type=int, default=5, help='The number of tasks in the set.')
    parser.add_argument('--uTotal', type=float, default=0.75, help='The total utilization of the task set.')
    parser.add_argument('--minsslength', type=float, default=0, help='Minimum suspension length as a ratio of (period - execution).')
    parser.add_argument('--maxsslength', type=float, default=0, help='Maximum suspension length as a ratio of (period - execution).')
    parser.add_argument('--Pmin', type=int, default=10, help='Minimum task period.')
    parser.add_argument('--numLog', type=int, default=1, help='The number of logarithmic decades for period distribution.')
    parser.add_argument('--vRatio', type=float, default=0, help='The ratio of tasks that have suspensions.')
    parser.add_argument('--seed', type=int, default=random.randint(1, 1000), help='The random seed for generation.')
    parser.add_argument('--numsegs', type=int, default=2, help='The number of execution segments.')
    parser.add_argument('--minSratio', type=int, default=1, help='Minimum ratio of suspension length to execution time.')
    parser.add_argument('--numpaths', type=int, default=2, help='The number of execution paths for each task.')
    parser.add_argument('--scalef', type=float, default=0.8, help="A scaling factor for sub-paths' execution and suspension times.")
    parser.add_argument('--plot_sets', action='store_true', help='Generate 100 tasksets and plot the results.')
    parser.add_argument('--printTasks', type=bool, default=False, help='Print the tasks sets')
    parser.add_argument('--ct_wcet_mult', type=float, default=1, help='Multiplier for the care-taking task\'s WCET.')
    parser.add_argument('--ct_d_down_mult', type=int, default=10, help='Multiplier for Delta_down.')
    parser.add_argument('--ct_d_up_mult', type=int, default=100, help='Multiplier for Delta_up.')
    parser.add_argument('--test_predefined', action='store_true', help='Test a predefined task set.')
    args = parser.parse_args()

    if args.test_predefined:
        test_predefined_feasibility()
    elif args.plot_sets:
        run_and_plot_tasksets(args)
    else:
        run_single_taskset(args)

def run_single_taskset(args):
    # Convert args to a dictionary to pass to taskGeneration_p
    params = vars(args).copy()
    params.pop('plot_sets', None)
    params.pop('printTasks', None)
    params.pop('ct_wcet_mult', None)
    params.pop('ct_d_down_mult', None)
    params.pop('ct_d_up_mult', None)
    params.pop('test_predefined', None)
    # Using a formatted string for better alignment
    for key, value in params.items():
        print(f"- {key:<20}: {value}")
    print("-" * 30)

    # Set the seed for reproducibility
    random.seed(params['seed'])

    # Generate the task set
    tasks = taskGeneration_p(**params)
    tasks.sort(key=lambda x: x['period'])

    print("\nGenerated Task Set:")
    for i, task in enumerate(tasks):
        # Pretty print the task dictionary
        print(f"Task {i}:")
        for key, value in task.items():
            # Don't print very long path details unless necessary
            if key == 'paths' and len(str(value)) > 100:
                 print(f"  - {key:<15}: [details omitted for brevity]")
            else:
                 print(f"  - {key:<15}: {value}")
    print("-" * 30)

    # Run the Suspension Oblivious schedulability test
    is_schedulable = SuspObl(tasks)

    # Print the results
    print("\n--- Schedulability Analysis ---")
    if is_schedulable:
        print("RESULT: The task set is SCHEDULABLE under the Suspension Oblivious test.")
        print("\nWorst-Case Response Times (WCRT):")
        for i, task in enumerate(tasks):
            print(f"Task {i}: {task['wcrt_obl']:.2f} (Deadline: {task['deadline']:.2f})")
    else:
        print("RESULT: The task set is NOT SCHEDULABLE under the Suspension Oblivious test.")
        print("\nAnalysis:")
        for i, task in enumerate(tasks):
            if 'wcrt_obl' in task:
                print(f"Task {i}: OK (WCRT: {task['wcrt_obl']:.2f} <= Deadline: {task['deadline']:.2f})")
            else:
                # This is the first task that failed the test.
                # We recompute its WCRT just to display it.
                wcrt = SuspObl_WCRT(task, tasks[:i])
                print(f"Task {i}: FAILED (WCRT: {wcrt:.2f} > Deadline: {task['deadline']:.2f})")
                break # No need to check lower priority tasks

    # Run the simple tests
    ll_schedulable = LiuAndLaylandBound(tasks)
    hb_schedulable = HyperbolicBound(tasks)
    tda_schedulable = TimeDemandAnalysis(tasks)

    print("\n--- Simple Schedulability Tests ---")
    print(f"Liu and Layland Bound: {'SCHEDULABLE' if ll_schedulable else 'TEST FAILED'}")
    print(f"Hyperbolic Bound: {'SCHEDULABLE' if hb_schedulable else 'TEST FAILED'}")
    if tda_schedulable:
        print("Time Demand Analysis: SCHEDULABLE")
        print("\nWorst-Case Response Times (TDA):")
        for i, task in enumerate(tasks):
            if 'wcrt' in task:
                print(f"Task {i}: {task['wcrt']:.2f} (Deadline: {task['deadline']:.2f})")
    else:
        print("Time Demand Analysis: NOT SCHEDULABLE")

def run_and_plot_tasksets(args):
    results = {
        #"Liu and Layland Bound": [],
        #"Hyperbolic Bound": [],
        "without care-taking": [],
        #"Liu and Layland Bound + CT(1,100,200)": [],
        #"Hyperbolic Bound + CT(1,100,200)": [],
        "arbitrary": [],
        "periodic": [],
        "sparse": [],
    }

    utilization_step = 0.01
    utilizations = np.arange(utilization_step, 1.0 + utilization_step, utilization_step)
    # give me an np array with only 0.5
    utilizations_40 = np.array([0.4])

    params = vars(args).copy()
    params.pop('plot_sets', None)
    params.pop('printTasks', None)
    params.pop('ct_wcet_mult', None)
    params.pop('ct_d_down_mult', None)
    params.pop('ct_d_up_mult', None)
    params.pop('test_predefined', None)

    time_to_find_T = {
            "Nr Tasks": [],
            "time": []
        }
    ignore_first_time_stamp = True

    # Create a directory name based on the arguments
    file_base_name = f"N-{args.NumberOfTasksPerSet}_CT-W{args.ct_wcet_mult}-Down{args.ct_d_down_mult}-Up{args.ct_d_up_mult}"
    plot_dir = os.path.join("careTaking", "plots")

    # Create the directory if it does not exist
    os.makedirs(plot_dir, exist_ok=True)


    for u in utilizations:
        print(f"Generating 10 task sets for utilization {u:.2f}")
        for i in range(1000):
            params['uTotal'] = u
            params['seed'] = random.randint(1, 10000)

            tasks = taskGeneration_p(**params)
            tasks.sort(key=lambda x: x['period'])

            ct_tasks = generate_care_taking_tasks(tasks, args.ct_wcet_mult, args.ct_d_down_mult, args.ct_d_up_mult)
            ct_rt_tasks = ct_to_rt_simple(tasks, ct_tasks)
            ct_rt_tasks_opt = ct_to_rt_simple_opt(tasks, ct_tasks)


            # Run tests
            ll_res = LiuAndLaylandBound(copy.deepcopy(tasks))
            hb_res = HyperbolicBound(copy.deepcopy(tasks))
            tda_res = TimeDemandAnalysis(copy.deepcopy(tasks))
            # Run test with ct tasks
            ll_res_ct = LiuAndLaylandBound_CT(copy.deepcopy(tasks), copy.deepcopy(ct_rt_tasks))
            hb_res_ct = HyperbolicBound_CT(copy.deepcopy(tasks), copy.deepcopy(ct_rt_tasks))
            tda_res_ct = TimeDemandAnalysis_CT(copy.deepcopy(tasks), copy.deepcopy(ct_rt_tasks))
            tda_res_ct_opt = TimeDemandAnalysis_CT(copy.deepcopy(tasks), copy.deepcopy(ct_rt_tasks_opt))


            # Measure time for subsequent executions
            start_time = time.time()
            T = find_largest_sparse_T(ct_tasks)
            elapsed_time = time.time() - start_time
            if not ignore_first_time_stamp:
                time_to_find_T["Nr Tasks"].append(len(ct_tasks))
                time_to_find_T["time"].append(elapsed_time)
            else:
                ignore_first_time_stamp = False

            # Print hat{T}
            if (T is not None) and args.printTasks:
                print(f"T: {T}")
            if T:
                ct_rt_tasks_sparse = ct_to_rt_sparse(ct_tasks, T)
                tda_res_sparese_ct = SparseWorkloadFunction_CT(copy.deepcopy(tasks), copy.deepcopy(ct_rt_tasks_sparse), copy.deepcopy(ct_tasks))
            else :
                tda_res_sparese_ct = False
                print(f"T: None")

            # nicely print rt and ct tasksets
            if args.printTasks:
                print("RT Taskset:")
                for task in tasks:
                    # only print execution and period
                    task = {'execution': task['execution'], 'period': task['period']}
                    print(task)
                print("CT Taskset:")
                for task in ct_tasks:
                    print(task)

            # Store results
            #results["Suspension Oblivious"].append((u, susp_obl_res))
            #results["Liu and Layland Bound"].append((u, ll_res))
            #results["Hyperbolic Bound"].append((u, hb_res))
            results["without care-taking"].append((u, tda_res))
            # Store results with ct
            #results["Suspension Oblivious + CT(1,100,200)"
            #results["Liu and Layland Bound + CT(1,100,200)"].append((u, ll_res_ct))
            #results["Hyperbolic Bound + CT(1,100,200)"].append((u, hb_res_ct))
            results["arbitrary"].append((u, tda_res_ct))
            results["periodic"].append((u, tda_res_ct_opt))
            results["sparse"].append((u, tda_res_sparese_ct))


    # Plot results
    plot_path = os.path.join(plot_dir, f"{file_base_name}.pdf")
    plot_tasksets(results, plot_path)

    # save time to compute T in csv file
    csv_path = os.path.join(plot_dir, f"{file_base_name}_time_T.csv")
    data = np.column_stack((time_to_find_T["Nr Tasks"], time_to_find_T["time"]))
    np.savetxt(csv_path, data, delimiter=",", fmt="%s", header="Nr Tasks, time", comments='')


if __name__ == "__main__":
    main()
