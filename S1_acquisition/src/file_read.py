import fiona
import pandas as pd
import geopandas as gpd
from typing import Union
from pathlib import Path
from fiona.drvsupport import supported_drivers

supported_drivers['LIBKML'] = 'rw'


def find_path_kml(path_relative_to_parent: str = "cron_task/last_downloaded.txt") -> str:
    """finds the filepath of the most recent .kml given the directory structure"""
    dir_parent = Path(__file__).parents[1]
    directory_download_names = Path.joinpath(dir_parent, path_relative_to_parent) 

    # read most recent kml file
    with open(directory_download_names) as file:
        lines = file.read().splitlines() 
        most_recent_file = lines[-1]
    filepath = Path.joinpath(dir_parent, f"data/{most_recent_file}.kml") 

    return filepath


def open_kml(filepath: str) -> gpd.geopandas.geodataframe.GeoDataFrame:
    """opens the kml and converts it to readable geodataframe"""
    gdf_list = []
    for layer in fiona.listlayers(filepath):    
        gdf = gpd.read_file(filepath, driver='LIBKML', layer=layer)
        gdf_list.append(gdf)
    gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))
    
    return gdf


def find_open_kml() -> Union[gpd.geopandas.geodataframe.GeoDataFrame, str]:
    """finds the relevant kml, opens it, and converts it to a geodataframe"""
    filepath = find_path_kml()
    
    print(f"Attempting to load {filepath}")

    gdf = open_kml(filepath=filepath)
    return gdf, filepath

if __name__ == '__main__':
    try:
        gdf = find_open_kml()
        print(f"Geodataframe extracted successfully")
    except Exception as e:
        print(e)
