import pandas as pd
from os import path
from utils import *

def main():
    if path.isfile('ratings.csv'):
        ratings = read_csv('ratings.csv')
    else:
        ratings = pd.DataFrame(columns=['Letterboxd URI', 'Name', 'Year'])

    if path.isfile('watched.csv'):
        watched = read_csv('watched.csv')
    else:
        watched = pd.DataFrame(columns=['Letterboxd URI', 'Name', 'Year'])

    if path.isfile('watchlist.csv'):
        watchlist = read_csv('watchlist.csv')
    else:
        watchlist = pd.DataFrame(columns=['Letterboxd URI', 'Name', 'Year'])
    
    merged_df = merge_dfs(ratings, watched, watchlist)
    print(merged_df)

if __name__ == '__main__':
    main()
