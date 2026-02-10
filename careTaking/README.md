# Care-Taking Task Schedulability Analysis

This directory contains implementations and tests for analyzing the schedulability of real-time systems with care-taking tasks. The implementation references theorems and lemmas from a main paper (referred to as `main.pdf` in the code comments).

## Files

### Core Logic
*   **`care_taking_task.py`**: Contains the core logic for care-taking tasks.
    *   Generates care-taking tasks based on WCET ratios and period multipliers.
    *   Implements conversion strategies from care-taking to real-time tasks (Simple, Simple Optimization, Sparse).
    *   Implements **Theorem 13** test (using Numba for performance) to check schedulability conditions.
    *   `find_largest_sparse_T`: Finds the largest valid $\hat{T}$ for the sparse model.

### Schedulability Tests
*   **`SimpleTests.py`**: Implements standard real-time schedulability tests:
    *   Liu and Layland Bound
    *   Hyperbolic Bound
    *   Time Demand Analysis (TDA)
    *   Calculation of Worst-Case Response Time (WCRT)
*   **`SimpleTests_ct.py`**: Implements schedulability tests adapted for care-taking tasks:
    *   `LiuAndLaylandBound_CT`: Liu & Layland bound including care-taking overhead.
    *   `HyperbolicBound_CT`: Hyperbolic bound including care-taking overhead.
    *   `TimeDemandAnalysis_CT`: TDA adapted for care-taking tasks.
    *   `SparseWorkloadFunction_CT`: Implements the sparse workload function analysis.

### Testing & Experiments
*   **`test_care_taking.py`**: Unit tests for the care-taking logic.
    *   Tests schedulability conditions (`SparseWorkloadFunction_CT`).
    *   Tests `find_largest_sparse_T` with various task configurations (valid $\hat{T}$, no $\hat{T}$, complex cases).
*   **`plot_time_experiments.py`**: script to analyze and visualize timing data from the `T_times_experiments` directory.
    *   Aggregates CSV data by number of tasks.
    *   Calculates statistics (mean, percentiles).
    *   Generates a box plot (`time_analysis_plot.png`) showing computation time vs. number of tasks.
*   **`plotting.py`**: Contains utility functions for plotting results.
    *   `plot_tasksets`: Plots Acceptance Ratio vs. Utilization for different tests.

## Usage

To run the unit tests:
```bash
python3 test_care_taking.py
```

To run the timing experiment analysis (assuming data exists in `T_times_experiments`):
```bash
python3 plot_time_experiments.py
```

## Dependencies
*   `numpy`
*   `matplotlib`
*   `scipy`
*   `numba`
