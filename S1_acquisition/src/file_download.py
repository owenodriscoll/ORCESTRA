import requests
from bs4 import BeautifulSoup
import os
import logging
from pathlib import Path
from typing import Union

from S1_acquisition.src.file_read import find_open_kml
from S1_acquisition.src.visualisation import plot_save_kml


url = "https://sentinel.esa.int/web/sentinel/copernicus/sentinel-1/acquisition-plans"
pattern = "s1a_mp_user"


path_relative_dir = Path(__file__).parents[1]
path_relative_dir.mkdir(parents=True, exist_ok=True)
directory_download = Path.joinpath(path_relative_dir, "data") 
files_downloaded = Path.joinpath(path_relative_dir, "cron_task/last_downloaded.txt") 
file_log = Path.joinpath(path_relative_dir, "cron_task/logfile.log") 


# Set up logging
logging.basicConfig(filename=file_log, level=logging.INFO, format='%(asctime)s %(message)s')


def get_downloaded_files() -> Union[None, list]:
    """Reads the file containing the list of all downloaded files."""
    if os.path.exists(files_downloaded):
        with open(files_downloaded, 'r') as file:
            return file.read().splitlines()  # Returns the list of downloaded files
    return []


def save_downloaded_file(file_name) -> None:
    """Appends a new downloaded file to the list."""
    with open(files_downloaded, 'a') as file:
        file.write(file_name + '\n')  # Append the new file to the list


def download_new_file(file_url, file_name, timeout: int = 60) -> None:
    logging.info(f"Attempting download from: {file_url}")
    response = requests.get(file_url, timeout=timeout)
    response.raise_for_status()
    
    # Save the new file
    file_download = Path.joinpath(directory_download,  file_name + ".kml")
    with open(file_download, 'wb') as file:
        file.write(response.content)
    logging.info(f"Downloaded new file: {file_name}")


def check_for_new_file():
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Find all the links with "s1a_mp_user" in the href (assumed pattern for download links)
    download_links = soup.find_all('a', href=lambda href: href and pattern in href)
    
    if download_links:
        # Get the first/latest link
        latest_link = download_links[0]
        latest_file_url = latest_link['href']
        if not latest_file_url.startswith("https"):
            latest_file_url = "https://sentinel.esa.int" + latest_file_url
        
        latest_file_name = os.path.basename(latest_file_url).upper()
        last_downloaded_file = get_downloaded_files()

        if latest_file_name not in last_downloaded_file:
            # Download the new file

            download_new_file(latest_file_url, latest_file_name)
            save_downloaded_file(latest_file_name)

            return True
        else:
            logging.info("No new file found. Latest file is up-to-date.")
    else:
        logging.info("No download links found containing 's1a_mp_user'.")

if __name__ == "__main__":

    bounds = [-75., 0., -0., 25.]

    logging.info("Script started.")
    try:
        new_download = check_for_new_file()
        
        if True:
            gdf, filename = find_open_kml() 
            plot_save_kml(gdf=gdf,
                          bounds=bounds)

    except Exception as e:
        logging.info(e)
    logging.info("Script finished.")

    

