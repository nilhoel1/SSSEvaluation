#!/usr/bin/env python3
"""
Plot script for analyzing timing experiments from T_times_experiments directory.
Reads all CSV files, aggregates data by number of tasks, and creates a plot with box plots
showing mean, standard deviation, and percentiles.

Box plot approach adapted from:
Source - https://stackoverflow.com/a/76783440
Posted by cottontail
Retrieved 2025-11-12, License - CC BY-SA 4.0
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def read_csv_file(filepath):
    """
    Read a CSV file and return arrays of number of tasks and times.

    Args:
        filepath: Path to CSV file

    Returns:
        tuple: (num_tasks array, times array)
    """
    data = np.genfromtxt(filepath, delimiter=',', skip_header=1)
    num_tasks = data[:, 0]
    times = data[:, 1]
    return num_tasks, times


def aggregate_data(data_dir):
    """
    Read all CSV files from the directory and aggregate by number of tasks.

    Args:
        data_dir: Directory containing CSV files

    Returns:
        dict: Dictionary with num_tasks as keys and list of times as values
    """
    # Find all CSV files
    csv_pattern = os.path.join(data_dir, "*.csv")
    csv_files = glob.glob(csv_pattern)

    print(f"Found {len(csv_files)} CSV files")

    # Dictionary to store all times for each number of tasks
    aggregated_data = {}

    # Read all files and aggregate
    for csv_file in csv_files:
        try:
            num_tasks, times = read_csv_file(csv_file)

            for n, t in zip(num_tasks, times):
                n_int = int(n)
                if n_int not in aggregated_data:
                    aggregated_data[n_int] = []
                aggregated_data[n_int].append(t)
        except Exception as e:
            print(f"Error reading {csv_file}: {e}")
            continue

    return aggregated_data


def calculate_statistics(aggregated_data):
    """
    Calculate mean and percentiles (1st, 25th, 75th, 99th) for each number of tasks.

    Args:
        aggregated_data: Dictionary with num_tasks as keys and list of times as values

    Returns:
        tuple: (num_tasks_sorted, means, p1, p25, p75, p99)
    """
    num_tasks_list = sorted(aggregated_data.keys())
    means = []
    p1_values = []
    p25_values = []
    p75_values = []
    p99_values = []

    for n in num_tasks_list:
        times_array = np.array(aggregated_data[n])
        means.append(np.mean(times_array))
        p1_values.append(np.percentile(times_array, 1))
        p25_values.append(np.percentile(times_array, 25))
        p75_values.append(np.percentile(times_array, 75))
        p99_values.append(np.percentile(times_array, 99))

    return np.array(num_tasks_list), np.array(means), np.array(p1_values), np.array(p25_values), np.array(p75_values), np.array(p99_values)


def plot_results(num_tasks, means, p1, p25, p75, p99, output_file=None):
    """
    Create a box plot showing statistics using matplotlib's bxp() method.
    Uses actual percentiles from the data.

    Args:
        num_tasks: Array of number of tasks
        means: Array of mean times
        p1: Array of 1st percentile times
        p25: Array of 25th percentile times
        p75: Array of 75th percentile times
        p99: Array of 99th percentile times
        output_file: Optional output file path to save the figure
    """
    fig, ax = plt.subplots(figsize=(12, 7))

    # Use 25th and 75th percentiles for the box boundaries
    q1 = p25
    q3 = p75

    # Use 1st and 99th percentiles for whiskers
    whislo = p1
    whishi = p99

    # Create the box plot data structure
    keys = ['med', 'q1', 'q3', 'whislo', 'whishi']
    box_stats = [dict(zip(keys, vals)) for vals in zip(means, q1, q3, whislo, whishi)]

    # Create positions for the boxes
    positions = list(range(1, len(num_tasks) + 1))

    # Plot the box plots
    bp = ax.bxp(box_stats, positions=positions, showfliers=False, widths=0.6,
                patch_artist=True,
                boxprops=dict(facecolor='lightblue', edgecolor='blue', linewidth=2),
                whiskerprops=dict(color='blue', linewidth=1.5),
                capprops=dict(color='blue', linewidth=1.5),
                medianprops=dict(color='red', linewidth=2))

    # Set x-axis labels to actual task numbers
    ax.set_xticks(positions)
    ax.set_xticklabels(num_tasks)

    ax.set_xlabel('Number of Tasks', fontsize=14, fontweight='bold')
    ax.set_ylabel('Time (seconds)', fontsize=14, fontweight='bold')
    ax.set_title('Computation Time vs Number of Tasks', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')

    # Add legend explaining the box plot components
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    legend_elements = [
        Patch(facecolor='lightblue', edgecolor='blue', label='25th-75th percentile (IQR)'),
        Line2D([0], [0], color='red', linewidth=2, label='Mean'),
        Line2D([0], [0], color='blue', linewidth=1.5, label='Whiskers (1st-99th percentile)')
    ]
    ax.legend(handles=legend_elements, fontsize=12, loc='best')

    # Use log scale if the range is large
    if np.max(means) / np.min(means) > 100:
        ax.set_yscale('log')
        ax.set_ylabel('Time (seconds, log scale)', fontsize=14, fontweight='bold')

    plt.tight_layout()

    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {output_file}")

    plt.show()


def print_statistics(num_tasks, means, p1, p25, p75, p99):
    """
    Print statistics table.

    Args:
        num_tasks: Array of number of tasks
        means: Array of mean times
        p1: Array of 1st percentile times
        p25: Array of 25th percentile times
        p75: Array of 75th percentile times
        p99: Array of 99th percentile times
    """
    print("\n" + "="*100)
    print(f"{'Tasks':<10} {'Mean (s)':<15} {'1st % (s)':<15} {'25th % (s)':<15} {'75th % (s)':<15} {'99th % (s)':<15}")
    print("="*100)
    for n, mean, p1_val, p25_val, p75_val, p99_val in zip(num_tasks, means, p1, p25, p75, p99):
        print(f"{n:<10} {mean:<15.6f} {p1_val:<15.6f} {p25_val:<15.6f} {p75_val:<15.6f} {p99_val:<15.6f}")
    print("="*100)


def main():
    """Main function to run the analysis and create the plot."""
    # Define the data directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "T_times_experiments")

    print(f"Reading data from: {data_dir}")

    # Aggregate data from all CSV files
    aggregated_data = aggregate_data(data_dir)

    if not aggregated_data:
        print("No data found!")
        return

    print(f"Found data for {len(aggregated_data)} different task counts")

    # Calculate statistics
    num_tasks, means, p1, p25, p75, p99 = calculate_statistics(aggregated_data)

    # Print statistics
    print_statistics(num_tasks, means, p1, p25, p75, p99)

    # Create output file path
    output_file = os.path.join(script_dir, "time_analysis_plot.png")

    # Create plot
    plot_results(num_tasks, means, p1, p25, p75, p99, output_file)


if __name__ == "__main__":
    main()
