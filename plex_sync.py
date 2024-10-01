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
    print(f"Searching for {name} ({year})")
    search_results = movie_library.search(title=name, year=year)
    if len(search_results) == 0:
        print(f"Movie not found: {name} ({year})")
        return None
    else:
        # Return the first result (best match)
        print(f"Found movie: {name} ({year})")
        return search_results[0]


def sync_movies(df: pd.DataFrame, config: dict):
    plex = setup_connection(config)

    # Get movie library and account
    library_name = config['PLEX']['movie_library']
    movie_library = plex.library.section(library_name)
    account = plex.myPlexAccount()

    for _, row in df.iterrows():
        name = row['Name']
        year = int(row['Year'])
        rating = row['Rating']
        watched = row['Watched']
        watchlist = row['Watchlist']

        # Search for movie
        movie = search_movie(movie_library, name, year)
        if movie is None:
            continue

        # Update rating
        if rating > 0 and movie.userRating != rating:
            movie.rate(rating)
            print(f"Rated {name} ({year}) with {rating} stars")

        # Update watched status
        if watched and not movie.isWatched:
            movie.markWatched()
            print(f"Marked {name} ({year}) as watched")

        # Update watchlist status
        if watchlist:
            try:
                account.addToWatchList(movie)
                print(f"Added {name} ({year}) to watchlist")
            except:
                # Already on watchlist
                pass
        