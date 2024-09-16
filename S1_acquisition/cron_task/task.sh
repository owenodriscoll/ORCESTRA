#!/bin/bash

# write out current crontab
crontab -l > mycron

if [ -z "$(conda info --base)" ]; then
  echo "No Conda environment is active."
else
  if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    # Linux or macOS
    path_conda="$(conda info --base)/bin/activate"
    separator="/"
  elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows (cygwin, msys, or native win32)
    path_conda="$((conda info --base)Scripts\\activate | sed 's/\//\\/g')"
    separator="\\"
  else
    echo "Unsupported OS: $OSTYPE"
    exit 1
  fi

  echo "Found Conda at: $path_conda"
fi

env=$CONDA_DEFAULT_ENV
echo "Activating conda environment: $env"

path_python=$(conda run -n $(basename $CONDA_PREFIX) which python) 
echo "Found Python at: $path_python"

# Get the directory of the current script (cron_task)
script_dir="$(dirname "$(realpath "$0")")"

# Define the relative path to the Python script
relative_path="../src/file_download.py"

# Construct the absolute path to the Python script
if [ "$separator" == "\\" ]; then
  # Windows uses backslashes
  path_script="$(echo "$script_dir/$relative_path" | sed 's/\//\\/g')"
else
  # Unix-like systems use forward slashes
  path_script="$(realpath "$script_dir/$relative_path")"
fi

echo "Found script at: $path_script"

# echo new cron task into cron file
echo "0 10 * * * source $path_conda $env && $path_python $path_script" >> mycron

# # for testing
# source $path_conda $env && $path_python $path_script

# install new cron file
crontab mycron
rm mycron
