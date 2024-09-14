import pandas as pd
from pathlib import Path
from datetime import datetime 


def find_dates_kml(filepath: str, date_format: str = "%Y%m%dT%H%M%S"):
    # find relavant date range
    date_start, date_end = filepath.stem.split("_")[-2:]

    # convert to datetime instance
    dt_start = datetime.strptime(date_start, date_format)
    dt_end =datetime.strptime(date_end, date_format)
    return dt_start, dt_end


def find_number_days_df(df, date_column: str):
    N_days = (df.iloc[-1][date_column] - df.iloc[0][date_column]).days
    return N_days


def find_start_date_df(df, date_column: str):
    start_date = df.iloc[0][date_column]
    return start_date