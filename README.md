Repository containing sub projects directly related to ORCESTRA campaign


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