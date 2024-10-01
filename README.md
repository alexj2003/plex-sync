# plex-sync

## Installation

```
git clone https://github.com/alexj2003/plex-sync
cd plex-sync
pip install -r requirements.txt
```

## Configuration

1. Make a copy of the configuration file:

```
# Windows
copy config_template.json config.json

# Linux
cp config_template.json config.json
```

2. Edit configuration file with the following:
    1. `url`: the URL that you'd use **on this machine** to connect directly to your Plex server (not a link to `app.plex.tv`).
    2. `token`: a [Plex Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/).
    3. `movie_library`: Name of your movie library. This is usually 'Movies' but may be named something different.

3. Export your [Personal Data](https://letterboxd.com/settings/data/) from Letterboxd, and copy the files `ratings.csv`, `watched.csv` and `watchlist.csv` into this folder.

## Running The App

```
python main.py
```
