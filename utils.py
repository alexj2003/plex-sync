import pandas as pd
from os import path

def read_csv(file_path):
    #Extract file name
    file_name = path.splitext(path.basename(file_path))[0]

    # Validate file name
    valid_names = ['ratings', 'watched', 'watchlist']
    if file_name not in valid_names:
        print(f"Invalid CSV file name: {file_name}. Must be one of {valid_names}")
        return None

    # Load CSV file
    df = pd.read_csv(file_path)

    # Exclude 'Letterboxd URI' column
    if 'Letterboxd URI' in df.columns:
        df.drop(columns=['Letterboxd URI'], inplace=True)
    
    return df
