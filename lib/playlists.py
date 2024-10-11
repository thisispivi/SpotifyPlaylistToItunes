import pandas as pd
import os


def rename_playlist_columns(df):
    columns = [
        "URI della traccia",
        "Nome della traccia",
        "URI dell'artista",
        "Nome dell'artista",
        "URI dell'album",
        "Nome dell'album",
        "URI dell'artista dell'album",
        "Nome dell'artista dell'album",
        "Data di rilascio dell'album",
        "URL dell'immagine dell'album",
        "Numero del disco",
        "Numero della traccia",
        "Durata della traccia (ms)",
        "URL di anteprima della traccia",
        "Esplicito",
        "Popolarità",
        "ISRC",
        "Aggiunto da",
        "Aggiunto il",
    ]
    new_columns = [
        "uri",
        "track_name",
        "artist_uri",
        "artist_name",
        "album_uri",
        "album_name",
        "album_artist_uri",
        "album_artist_name",
        "album_release_date",
        "album_image_url",
        "disc_number",
        "track_number",
        "track_duration_ms",
        "track_preview_url",
        "explicit",
        "popularity",
        "isrc",
        "added_by",
        "added_at",
    ]

    df.rename(columns=dict(zip(columns, new_columns)), inplace=True)
    return df


def merge_all_playlists(root_dir):
    csv_dir = os.path.join(root_dir, "playlists")

    final_df = pd.DataFrame()
    files = os.listdir(csv_dir)
    for file in files:
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(csv_dir, file))
            final_df = pd.concat([final_df, df])

    return final_df.drop_duplicates(subset=["URI della traccia"])


def split_by_release_decade(root_dir, df):
    dataset_dir = os.path.join(root_dir, "datasets")

    df["album_release_date"] = df["album_release_date"].str[:4]
    df.dropna(subset=["album_release_date"], inplace=True)

    for decade in range(1950, 2030, 10):
        print(f"Creating dataset for {decade}s")
        decade_df = df[
            (df["album_release_date"].astype(int) >= decade)
            & (df["album_release_date"].astype(int) < decade + 10)
        ]
        decade_df.to_csv(os.path.join(dataset_dir, f"{decade}s.csv"), index=False)

    return df


def add_random_date(df):
    import random
    import datetime

    num_rows = df.shape[0]
    curr_date = datetime.datetime.now()
    guess_dates = []
    for i in range(num_rows):
        guess_dates.append(curr_date + datetime.timedelta(days=i))

    print(num_rows)
    random.shuffle(guess_dates)

    df["guess_date"] = guess_dates

    return df


def add_random_date_to_all_datasets(root_dir):
    dataset_dir = os.path.join(root_dir, "datasets")
    files = os.listdir(dataset_dir)
    for file in files:
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(dataset_dir, file))
            df = add_random_date(df)
            df.to_csv(os.path.join(dataset_dir, file), index=False)


def remove_less_than_1min_songs(df):
    df = df[df["track_duration_ms"] > 90000]
    return df


def generate_dataset(root_dir):
    df = merge_all_playlists(root_dir)
    df = rename_playlist_columns(df)
    df = remove_less_than_1min_songs(df)
    return df
