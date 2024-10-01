from plexapi.exceptions import BadRequest
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

def get_playlist(plex: PlexServer, playlist_name: str, config: dict) -> Playlist:
    # Get movie library
    library_name = config['PLEX']['movie_library']
    movie_library = plex.library.section(library_name)

    # Try to load existing playlist, otherwise create new one
    try:
        playlist = plex.playlist(playlist_name)
        print(f"Using existing playlist: {playlist_name}")
    except BadRequest:
        playlist = movie_library.createPlaylist(playlist_name)
        print(f"Creating new playlist: {playlist_name}")

    return playlist

def add_to_playlist(plex: PlexServer, playlist: Playlist, movies: pd.DataFrame, config: dict):
    # Get movie library
    library_name = config['PLEX']['movie_library']
    movie_library = plex.library.section(library_name)

    # Add movies to playlist
    existing_items = playlist.items()
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
        if movie is None or movie in existing_items:
            continue

        print(f"Adding {movie_title} to playlist")
        movies_to_add.append(movie)

    # Add movies to playlist
    if len(movies_to_add) == 0:
        print("No movies to add to playlist")
    else:
        try:
            playlist.addItems(movies_to_add)
        except BadRequest:
            print(f"Failed to add movies to playlist: {playlist.title}. Ensure that playlist is not a smart playlist.")
