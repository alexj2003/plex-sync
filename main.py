import pandas as pd
from os import getcwd, listdir, path
from globals import VALID_NAMES, PLAYLIST_PATH
from plex_sync import *
from utils import *

def main():
    # Read CSV files
    dataframes = []
    for name in VALID_NAMES:
        file_path = path.join(globals.DATA_PATH, f"{name}.csv")
        if path.isfile(file_path):
            print(f"Reading {name}.csv")
            df = read_csv(file_path)
        else:
            # Not found, create empty dataframe
            print(f"{name}.csv not found")
            df = pd.DataFrame(columns=['Letterboxd URI', 'Name', 'Year'])
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

    # Initialise Plex connection
    plex = setup_connection(config)

    # Sync movies
    sync_movies(plex, merged_df, config)

    # Read playlists
    playlist_path = path.join(getcwd(), PLAYLIST_PATH)
    for file in listdir(playlist_path):
        if file.endswith('.csv'):
            print()
            print(f"Reading playlist: {file}")
            playlist_file = path.join(PLAYLIST_PATH, file)
            list_name, list_movies = read_csv_letterboxd_list(playlist_file)

            # Delete the playlist if it already exists
            delete_playlist_if_exists(plex, list_name)

            # Add movies to playlist
            add_to_playlist(plex, list_name, list_movies, config)

    # Output statistics
    output_statistics()

if __name__ == '__main__':
    main()
