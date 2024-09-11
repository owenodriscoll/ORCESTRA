#write out current crontab
crontab -l > mycron

#set variables
env="env_colocate"      # <-- environment with necessary packages
path_base="/Users/opodriscoll"      # <-- custom base bath
path_conda="$path_base/miniconda3/bin/activate"      # <-- conda location
path_python="$path_base/miniconda3/envs/$env/bin/python"      # <-- python location
path_script="$path_base/Documents/Scripts/ORCESTRA/S1_acquisition/src/file_download.py"      # <-- python script location

#echo new cron task into cron file
echo "00 10 * * * source $path_conda $env && $path_python $path_script" >> mycron

#install new cron file
crontab mycron
rm mycron