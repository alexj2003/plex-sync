import pandas as pd
from os import path
from plex_sync import sync_movies
from utils import *

def main():
    # Read CSV files
    if path.isfile('ratings.csv'):
        ratings = read_csv('ratings.csv')
    else:
        print("ratings.csv not found")
        ratings = pd.DataFrame(columns=['Letterboxd URI', 'Name', 'Year'])

    if path.isfile('watched.csv'):
        watched = read_csv('watched.csv')
    else:
        print("watched.csv not found")
        watched = pd.DataFrame(columns=['Letterboxd URI', 'Name', 'Year'])

    if path.isfile('watchlist.csv'):
        watchlist = read_csv('watchlist.csv')
    else:
        print("watchlist.csv not found")
        watchlist = pd.DataFrame(columns=['Letterboxd URI', 'Name', 'Year'])
    
    # Merge dataframes
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
