import matplotlib.pyplot as plt
import numpy as np

def plot_tasksets(data, output_path):
    """
    Plots the acceptance ratio vs. utilization.
    Data is a dictionary where keys are test names and values are lists of tuples (utilization, schedulable).
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.9, left=0.1, right=0.95, hspace=0.3)

    ax.set_xlabel('Utilization (%)', size=15)
    ax.set_ylabel('Acceptance Ratio', size=15)
    ax.spines['top'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.tick_params(labelcolor='black', top=False, bottom=False, left=False, right=False)

    utilizations = sorted(list(set([d[0] for d in data[list(data.keys())[0]]])))

    for test_name, results in data.items():
        acceptance_ratios = []
        for u in utilizations:
            total = 0
            schedulable = 0
            for res_u, res_sched in results:
                if round(res_u, 2) == round(u, 2):
                    total += 1
                    if res_sched:
                        schedulable += 1

            acceptance_ratios.append(schedulable / total if total > 0 else 0)

        markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h']
        marker_idx = list(data.keys()).index(test_name) % len(markers)
        ax.plot([u * 100 for u in utilizations], acceptance_ratios, marker=markers[marker_idx], linestyle='-', label=test_name, clip_on=False)

    #ax.legend(bbox_to_anchor=(0.5, 1.11), loc=10, markerscale=1.5, ncol=len(data), borderaxespad=0., prop={'size': 10})
    ax.grid()

    fig.savefig(output_path, bbox_inches='tight')
    print(f'[DONE] {output_path}')
