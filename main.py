import pandas as pd
from os import path
from utils import *

def main():
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
    
    merged_df = merge_dfs(ratings, watched, watchlist)
    print(merged_df)

    if path.isfile('config.json'):
        config = read_config('config.json')
        print(config)
    else:
        print("config.json not found")
        exit(1)

if __name__ == '__main__':
    main()
