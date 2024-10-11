from lib.playlists import (
    generate_dataset,
    split_by_release_decade,
    add_random_date_to_all_datasets,
)
from lib.identify import identify
import os

root_dir = os.path.dirname(__file__)


if __name__ == "__main__":
    df = generate_dataset(root_dir)
    identifiers = identify(df)
    df["itunes_identifier"] = identifiers
    df = split_by_release_decade(root_dir, df)
    add_random_date_to_all_datasets(root_dir)
