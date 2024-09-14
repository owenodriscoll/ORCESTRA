Repository containing sub projects directly related to ORCESTRA campaign

- S1_acquistion: downloads and visualizes the latest Sentinel-1 acquistion plan

## Run Cronjob

Create the correct environment

`conda create -n ENVNAME python=3.12`

`conda activate ENVNAME`

Navigate to the correct directory

`cd ORCESTRA`

Install packages within `pyproject.toml`

`pip install -e .`

Go to `S1_acquisition/cron_task/task.sh` and set paths and update frequency

Run Bash script

`bash path/to/S1_acquisition/cron_task/task.sh`

This will start a recurring cron job scheduled for 10 am every day that looks for and downloads/visualizes updated acquistion plans