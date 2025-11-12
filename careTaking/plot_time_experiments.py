#!/usr/bin/env python3
"""
Plot script for analyzing timing experiments from T_times_experiments directory.
Reads all CSV files, aggregates data by number of tasks, and creates a plot with error bars
showing mean, standard deviation, min, and max values.
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt


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
    Calculate mean, std, 1st percentile, 99th percentile for each number of tasks.

    Args:
        aggregated_data: Dictionary with num_tasks as keys and list of times as values

    Returns:
        tuple: (num_tasks_sorted, means, stds, p1, p99)
    """
    num_tasks_list = sorted(aggregated_data.keys())
    means = []
    stds = []
    p1_values = []
    p99_values = []

    for n in num_tasks_list:
        times_array = np.array(aggregated_data[n])
        means.append(np.mean(times_array))
        stds.append(np.std(times_array))
        p1_values.append(np.percentile(times_array, 1))
        p99_values.append(np.percentile(times_array, 99))

    return np.array(num_tasks_list), np.array(means), np.array(stds), np.array(p1_values), np.array(p99_values)


def plot_results(num_tasks, means, stds, p1, p99, output_file=None):
    """
    Create a plot with error bars showing statistics.

    Args:
        num_tasks: Array of number of tasks
        means: Array of mean times
        stds: Array of standard deviations
        p1: Array of 1st percentile times
        p99: Array of 99th percentile times
        output_file: Optional output file path to save the figure
    """
    fig, ax = plt.subplots(figsize=(12, 7))

    # Calculate error bar values
    # Standard deviation error bars (symmetric)
    yerr_std = stds

    # Percentile error bars (asymmetric)
    # Lower error: distance from mean to 1st percentile
    # Upper error: distance from 99th percentile to mean
    yerr_percentile_lower = means - p1
    yerr_percentile_upper = p99 - means
    yerr_percentile = [yerr_percentile_lower, yerr_percentile_upper]

    # Plot mean with standard deviation error bars (no connecting line)
    ax.errorbar(num_tasks, means, yerr=yerr_std, fmt='s', capsize=5, capthick=2,
                label='Mean ± Std Dev', linewidth=0, markersize=10,
                color='blue', elinewidth=2, alpha=0.7)

    # Plot mean with percentile error bars (no connecting line)
    ax.errorbar(num_tasks, means, yerr=yerr_percentile, fmt='s', capsize=7, capthick=2,
                label='Mean (1st-99th percentile)', linewidth=0, markersize=8,
                color='red', elinewidth=2, alpha=0.6)

    ax.set_xlabel('Number of Tasks', fontsize=14, fontweight='bold')
    ax.set_ylabel('Time (seconds)', fontsize=14, fontweight='bold')
    ax.set_title('Computation Time vs Number of Tasks', fontsize=16, fontweight='bold')
    ax.legend(fontsize=12, loc='best')
    ax.grid(True, alpha=0.3, linestyle='--')

    # Use log scale if the range is large
    if np.max(means) / np.min(means) > 100:
        ax.set_yscale('log')
        ax.set_ylabel('Time (seconds, log scale)', fontsize=14, fontweight='bold')

    plt.tight_layout()

    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {output_file}")

    plt.show()


def print_statistics(num_tasks, means, stds, p1, p99):
    """
    Print statistics table.

    Args:
        num_tasks: Array of number of tasks
        means: Array of mean times
        stds: Array of standard deviations
        p1: Array of 1st percentile times
        p99: Array of 99th percentile times
    """
    print("\n" + "="*90)
    print(f"{'Tasks':<10} {'Mean (s)':<15} {'Std Dev (s)':<15} {'1st % (s)':<15} {'99th % (s)':<15}")
    print("="*90)
    for n, mean, std, p1_val, p99_val in zip(num_tasks, means, stds, p1, p99):
        print(f"{n:<10} {mean:<15.6f} {std:<15.6f} {p1_val:<15.6f} {p99_val:<15.6f}")
    print("="*90)


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
    num_tasks, means, stds, p1, p99 = calculate_statistics(aggregated_data)

    # Print statistics
    print_statistics(num_tasks, means, stds, p1, p99)

    # Create output file path
    output_file = os.path.join(script_dir, "time_analysis_plot.png")

    # Create plot
    plot_results(num_tasks, means, stds, p1, p99, output_file)


if __name__ == "__main__":
    main()
