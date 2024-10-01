import json
import numpy as np
import pandas as pd
from os import path
from constants import VALID_NAMES

def read_csv(file_path: str) -> pd.DataFrame:
    #Extract file name
    file_name = path.splitext(path.basename(file_path))[0]

    # Validate file name
    if file_name not in VALID_NAMES:
        print(f"Invalid CSV file name: {file_name}. Must be one of {VALID_NAMES}")
        return None

    # Load CSV file
    df = pd.read_csv(file_path)

    return df

def read_csv_letterboxd_list(file_path: str) -> pd.DataFrame:
    # Load CSV file
    df = pd.read_csv(file_path, skiprows=1)

    # Extract list name from metadata
    list_name = df['Name'][0]

    # Extract movies
    list_movies = pd.read_csv(file_path, skiprows=4)

    return list_name, list_movies

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
    merged_df = pd.merge(ratings, watched, how='outer', on=['Letterboxd URI', 'Name', 'Year', 'Rating', 'Watched', 'Watchlist'])
    merged_df = pd.merge(merged_df, watchlist, how='outer', on=['Letterboxd URI', 'Name', 'Year', 'Rating', 'Watched', 'Watchlist'])

    # Fill NaN values
    merged_df['Watched'] = merged_df['Watched'].fillna(False)
    merged_df['Watchlist'] = merged_df['Watchlist'].fillna(False)
    merged_df['Rating'] = merged_df['Rating'].fillna(0)

    # Remove duplicate rows
    merged_df = merged_df.drop_duplicates(subset='Letterboxd URI')

    # Modify ratings (Plex uses 1-10)
    merged_df['Rating'] = merged_df['Rating'] * 2
    merged_df['Rating'] = merged_df['Rating'].clip(upper=10, lower=0)

    # Return only needed columns
    merged_df = merged_df[['Name', 'Year', 'Watched', 'Watchlist', 'Rating']]
    return merged_df

def read_config(file_path: str) -> dict:
    with open(file_path) as f:
        config = json.load(f)

    return config
