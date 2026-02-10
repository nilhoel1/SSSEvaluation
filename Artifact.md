# Artifact evaluation for care taking Schedulability

This Repository contains the SSSEvaluation suite.
All tasks used for the paper "Releaser Design and Schedulability Analysis for Care-Taking Tasks in Real-Time Systems" are in the careTaking folder.

## Setup

To recreate the experiments, you first need to set up the Python environment.

1.  **Create a virtual environment:**
    The scripts assume the virtual environment is located at `.venv` in the root of the repository.
    ```bash
    python3 -m venv .venv
    ```

2.  **Install dependencies:**
    Activate the virtual environment and install the required packages.
    ```bash
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

    *Note: The project uses Gurobi (`gurobipy`). Ensure you have a valid Gurobi license if required, or that the problem sizes fit within the trial license limits.*

## Recreating Experiment 1: Schedulability Analysis (Fig. 5)

This experiment runs multiple configurations to generate the schedulability plots shown in Figure 5 of the paper.

1.  **Run the experiment script:**
    Execute the `run_paper_experiments.sh` script. This will launch several background processes to run the variations in parallel.
    ```bash
    ./run_paper_experiments.sh
    ```

2.  **View Results:**
    Once the script completes, the generated plots will be available in the `careTaking/plots` directory.

## Recreating Experiment 2: Timing Analysis (Fig. 4)
**Warining** Compute intensive!

This experiment evaluates the runtime performance of the analysis.
**Note:** The resulting figure might differ from the paper as runtime is dependent on the specific compute hardware (e.g., local machine vs. valid compute server). To save time reduce the Number of tasks in the script.

1.  **Run the variations:**
    Execute the `run_all_variations.sh` script. This runs a comprehensive set of experiments to gather timing data.
    ```bash
    ./run_all_variations.sh
    ```
    *You can optionally specify the number of parallel processes as an argument (e.g., `./run_all_variations.sh 4`), otherwise, it uses all available cores.*

2.  **Process the Data:**
    The experiment generates `.csv` files in the `plots` directory (or `careTaking/plots` depending on how it's configured). You need to move these files to the `careTaking/T_times_experiments` directory for the plotting script to find them.
    ```bash
    # Move the generated CSV files
    mv careTaking/plots/*_time_T.csv careTaking/T_times_experiments/
    ```

3.  **Generate the Plot:**
    Run the plotting script to generate Figure 4.
    ```bash
    python3 careTaking/plot_time_experiments.py
    ```
    The resulting plot will be saved as `careTaking/time_analysis_plot.png`.
