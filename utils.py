import json
import numpy as np
import pandas as pd
from os import path

def read_csv(file_path: str) -> pd.DataFrame:
    #Extract file name
    file_name = path.splitext(path.basename(file_path))[0]

    # Validate file name
    valid_names = ['ratings', 'watched', 'watchlist']
    if file_name not in valid_names:
        print(f"Invalid CSV file name: {file_name}. Must be one of {valid_names}")
        return None

    # Load CSV file
    df = pd.read_csv(file_path)

    return df

def merge_dfs(ratings: pd.DataFrame, watched: pd.DataFrame, watchlist: pd.DataFrame) -> pd.DataFrame:
    # Prepare dataframes
    ratings['Watched'] = True
    ratings['Watchlist'] = np.nan

    watched['Rating'] = np.nan
    watched['Watched'] = True
    watched['Watchlist'] = np.nan

    watchlist['Rating'] = np.nan
    watchlist['Watched'] = np.nan
    watchlist['Watchlist'] = True

    # Merge dataframes
    merged_df = pd.merge(ratings, watched, how='outer', on=['Letterboxd URI', 'Name', 'Year'])
    merged_df = pd.merge(merged_df, watchlist, how='outer', on=['Letterboxd URI', 'Name', 'Year'])

    # Fill NaN values
    merged_df['Watched'] = merged_df['Watched'].fillna(False)
    merged_df['Watchlist'] = merged_df['Watchlist'].fillna(False)
    merged_df['Rating'] = merged_df['Rating'].fillna(0)

    merged_df = merged_df[['Name', 'Year', 'Watched', 'Watchlist', 'Rating']]
    return merged_df

def read_config(file_path: str) -> dict:
    with open(file_path) as f:
        config = json.load(f)

    return config
