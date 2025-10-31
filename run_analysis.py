import random
import argparse
from schedTest.tgPath import taskGeneration_p
from schedTest.FixedPriority import SuspObl, SuspObl_WCRT
from schedTest.SimpleTests import LiuAndLaylandBound, HyperbolicBound, TimeDemandAnalysis

def main():
    """
    This script generates a task set using tgPath.py and checks its
    schedulability using the Suspension Oblivious test from FixedPriority.py.
    """
    parser = argparse.ArgumentParser(description="Generate and test a task set.")
    parser.add_argument('--NumberOfTasksPerSet', type=int, default=5, help='The number of tasks in the set.')
    parser.add_argument('--uTotal', type=float, default=0.75, help='The total utilization of the task set.')
    parser.add_argument('--minsslength', type=float, default=0.1, help='Minimum suspension length as a ratio of (period - execution).')
    parser.add_argument('--maxsslength', type=float, default=0.3, help='Maximum suspension length as a ratio of (period - execution).')
    parser.add_argument('--Pmin', type=int, default=100, help='Minimum task period.')
    parser.add_argument('--numLog', type=int, default=1, help='The number of logarithmic decades for period distribution.')
    parser.add_argument('--vRatio', type=float, default=1, help='The ratio of tasks that have suspensions.')
    parser.add_argument('--seed', type=int, default=random.randint(1, 1000), help='The random seed for generation.')
    parser.add_argument('--numsegs', type=int, default=2, help='The number of execution segments.')
    parser.add_argument('--minSratio', type=int, default=1, help='Minimum ratio of suspension length to execution time.')
    parser.add_argument('--numpaths', type=int, default=2, help='The number of execution paths for each task.')
    parser.add_argument('--scalef', type=float, default=0.8, help="A scaling factor for sub-paths' execution and suspension times.")
    args = parser.parse_args()

    # Convert args to a dictionary to pass to taskGeneration_p
    params = vars(args)

    print("Generating task set with the following parameters:")
    # Using a formatted string for better alignment
    for key, value in params.items():
        print(f"- {key:<20}: {value}")
    print("-" * 30)

    # Set the seed for reproducibility
    random.seed(params['seed'])

    # Generate the task set
    tasks = taskGeneration_p(**params)

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
    print(f"Liu and Layland Bound: {'SCHEDULABLE' if ll_schedulable else 'NOT SCHEDULABLE'}")
    print(f"Hyperbolic Bound: {'SCHEDULABLE' if hb_schedulable else 'NOT SCHEDULABLE'}")
    if tda_schedulable:
        print("Time Demand Analysis: SCHEDULABLE")
        print("\nWorst-Case Response Times (TDA):")
        for i, task in enumerate(tasks):
            print(f"Task {i}: {task['wcrt']:.2f} (Deadline: {task['deadline']:.2f})")
    else:
        print("Time Demand Analysis: NOT SCHEDULABLE")


if __name__ == "__main__":
    main()
