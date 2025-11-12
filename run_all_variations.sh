#!/bin/bash

# Check if the number of parallel processes is provided
if [ -z "$1" ]; then
  # If not, use the number of available cores
  if [[ "$(uname)" == "Darwin" ]]; then
    NUM_PARALLEL=$(sysctl -n hw.ncpu)
  else
    NUM_PARALLEL=$(nproc)
  fi
  echo "Number of parallel processes not specified. Using $NUM_PARALLEL cores." > /dev/null
else
  NUM_PARALLEL=$1
fi

# Check if the python executable is provided
if [ -z "$2" ]; then
  PYTHON_EXEC="python3"
  echo "Python executable not specified. Using $PYTHON_EXEC."
else
  PYTHON_EXEC=$2
fi

# Define the arrays of parameters to test
WCETMul=(0.5 1 1.5 5 10)
Delta_upMul=(10 25 50 100 200)
Delta_DownMul=(5 10 25 50 100)
NrTasks=(2 5 25 50 100)

# Create a command for each combination of parameters
for wcet in "${WCETMul[@]}"; do
  for up_idx in "${!Delta_upMul[@]}"; do
    for down_idx in "${!Delta_DownMul[@]}"; do
      if (( down_idx < up_idx )); then
        continue
      fi
      up=${Delta_upMul[$up_idx]}
      down=${Delta_DownMul[$down_idx]}
      for tasks in "${NrTasks[@]}"; do
        echo "{ echo 'Running with WCETMul=$wcet, Delta_upMul=$up, Delta_DownMul=$down, NrTasks=$tasks'; $PYTHON_EXEC run_careTaking.py --plot_sets --NumberOfTasksPerSet '$tasks' --ct_wcet_mult '$wcet' --ct_d_up_mult '$up' --ct_d_down_mult '$down' ;} > /dev/null"
      done
    done
  done
done | xargs -P "$NUM_PARALLEL" -I {} bash -c "{}"

echo "All variations have been processed." > /dev/null
