# Artifact evaluation for care taking Schedulability

This Repository contains the SSSEvaluation suite.
All tasks used for the paper "Releaser Design and Schedulability Analysis for Care-Taking Tasks in Real-Time Systems" are in the careTaking folder.

## Setup

To recreate the experiments, you first need to set up the Python environment.
This artifact was evaluated using **Python 3.14.3**. The following steps should also be followed, when using the devcontainer in vsCode, which we recommend!

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

    **Note for Python 3.14+:** Due to a version conflict in the `mip` package (which pins an old `cffi`), you must install it manually without dependencies:
    ```bash
    pip install --no-deps mip>=1.14.2
    ```

    *Note: The project uses Gurobi (`gurobipy`). But it is not used, so setting up a Gurobi license for this is not necessary.

## Recreating Experiment 1: Schedulability Analysis (Fig. 5)

This experiment runs multiple configurations to generate the schedulability plots shown in Figure 5 of the paper.

1.  **Run the experiment script:**
    Ensure the script is executable and run it. This will launch several background processes to run the variations in parallel.
    ```bash
    chmod +x run_paper_experiments.sh
    ./run_paper_experiments.sh
    ```

2.  **View Results:**
    Once the script completes, the generated plots will be available in the `careTaking/plots` directory.

## Recreating Experiment 2: Timing Analysis (Fig. 4)
**Warining** Compute intensive!

This experiment evaluates the runtime performance of the analysis.
**Note:** The resulting figure might differ from the paper as runtime is dependent on the specific compute hardware (e.g., local machine vs. valid compute server). To save time reduce the Number of tasks in the script.

1.  **Run the variations:**
    Ensure the script is executable and run the variations. It is recommended to pass the virtual environment's python path to ensure all dependencies are found.
    ```bash
    chmod +x run_all_variations.sh
    ./run_all_variations.sh "" ./.venv/bin/python3
    ```
    *You can optionally specify the number of parallel processes as the first argument (e.g., `./run_all_variations.sh 4 ./.venv/bin/python3`).*

2.  **Process the Data:**
    The experiment generates `.csv` files in the `careTaking/plots` directory. Create the target directory and move the files there.
    ```bash
    # Create the directory if it doesn't exist
    mkdir -p careTaking/T_times_experiments

    # Move the generated CSV files
    mv careTaking/plots/*_time_T.csv careTaking/T_times_experiments/
    ```

3.  **Generate the Plot:**
    Run the plotting script to generate Figure 4.
    ```bash
    ./.venv/bin/python3 careTaking/plot_time_experiments.py
    ```
    The resulting plot will be saved as `careTaking/time_analysis_plot.png`.
