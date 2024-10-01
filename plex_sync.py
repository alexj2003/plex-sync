from plexapi.exceptions import BadRequest, NotFound
from plexapi.playlist import Playlist
from plexapi.server import PlexServer
import pandas as pd

def setup_connection(config: dict) -> PlexServer:
    # Connect to Plex server
    url = config['PLEX']['url']
    token = config['PLEX']['token']
    plex = PlexServer(url, token)

    return plex

def search_movie(movie_library, name: str, year: int):
    # Search for movie
    print()
    if year is None:
        movie_title = name
        search_results = movie_library.search(title=name)
    else:
        movie_title = f"{name} ({year})"
        search_results = movie_library.search(title=name, year=year)
    print(f"Searching for {movie_title}")
    if len(search_results) == 0:
        print(f"Movie not found: {movie_title}")
        return None
    else:
        # Return the first result (best match)
        print(f"Found movie: {movie_title}")
        return search_results[0]

def sync_movies(plex: PlexServer, df: pd.DataFrame, config: dict):
    # Get movie library and account
    library_name = config['PLEX']['movie_library']
    movie_library = plex.library.section(library_name)
    account = plex.myPlexAccount()

    for _, row in df.iterrows():
        name = row['Name']
        year = int(row['Year']) if not pd.isnull(row['Year']) else None
        rating = row['Rating']
        watched = row['Watched']
        watchlist = row['Watchlist']

        if year is None:
            movie_title = f"{name}"
        else:
            movie_title = f"{name} ({year})"

        # Search for movie
        movie = search_movie(movie_library, name, year)
        if movie is None:
            continue

        # Update rating
        if rating > 0 and movie.userRating != rating:
            movie.rate(rating)
            print(f"Rated {movie_title} with {rating}/10.0")

        # Update watched status
        if watched and not movie.isWatched:
            movie.markWatched()
            print(f"Marked {movie_title}) as watched")

        # Update watchlist status
        if watchlist:
            try:
                account.addToWatchlist(movie)
                print(f"Added {movie_title} to watchlist")
            except BadRequest:
                # Already on watchlist
                pass

def delete_playlist_if_exists(plex: PlexServer, playlist_name: str):
    # Delete the playlist if it already exists
    try:
        playlist = plex.playlist(playlist_name)
        playlist.delete()
        print(f"Playlist found, deleting: {playlist_name}")
    except NotFound:
        # Playlist not found, we can create it later
        pass

def add_to_playlist(plex: PlexServer, list_name: str, movies: pd.DataFrame, config: dict):
    # Get movie library
    library_name = config['PLEX']['movie_library']
    movie_library = plex.library.section(library_name)

    # Add movies to playlist
    movies_to_add = []
    for _, row in movies.iterrows():
        name = row['Name']
        year = int(row['Year']) if not pd.isnull(row['Year']) else None

        if year is None:
            movie_title = f"{name}"
        else:
            movie_title = f"{name} ({year})"

        # Search for movie
        movie = search_movie(movie_library, name, year)
        if movie is None:
            continue

        print(f"Adding {movie_title} to playlist")
        movies_to_add.append(movie)

    # Add movies to playlist
    if len(movies_to_add) == 0:
        print("No movies to add to playlist")
    else:
        print(f"Creating playlist: {list_name}")
        movie_library.createPlaylist(list_name, items=movies_to_add)