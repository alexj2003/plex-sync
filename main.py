import pandas as pd
from os import path
from plex_sync import sync_movies
from constants import *
from utils import *

def main():
    # Read CSV files
    dataframes = []
    for name in VALID_NAMES:
        file_path = path.join(DATA_PATH, f"{name}.csv")
        if path.isfile(file_path):
            df = read_csv(file_path)
            print(f"Read {name}.csv")
        else:
            # Not found, create empty dataframe
            df = pd.DataFrame(columns=['Letterboxd URI', 'Name', 'Year'])
            print(f"{name}.csv not found")
        dataframes.append(df)

    # Merge dataframes
    ratings, watched, watchlist = dataframes
    merged_df = merge_dfs(ratings, watched, watchlist)

    # Read config
    if path.isfile('config.json'):
        config = read_config('config.json')
    else:
        print("config.json not found")
        exit(1)

    # Sync movies
    sync_movies(merged_df, config)

if __name__ == '__main__':
    main()
