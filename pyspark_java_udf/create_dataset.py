import numpy as np
import os
import pandas as pd

from tqdm import tqdm

# fmt: off
DATASETS = [
    (3, 10),
    (4, 20),
    (5, 50),
    (6, 100),
    (7, 200),
    (8, 500)
]
# fmt: on


def create_one_dataset(order, num_files):
    """
        Creates some files that will contain latitude and longitude data
        
        Args:
            order: exponent of the total number of rows (10**order)
            num_files: number of parquets files in the dataset
    """

    rows = 10 ** order
    rows_file = rows // num_files

    # Create dataset folder
    folder = f"data/dataset_{order}"
    os.makedirs(folder, exist_ok=True)

    for i in tqdm(range(num_files), desc=f"order_{order}"):
        # Create the dataframe
        df = pd.DataFrame(np.random.rand(rows_file, 2), columns=["latitude", "longitude"])

        # Set correct ranges for latitude and longitude
        df["latitude"] = df["latitude"] * 180 - 90
        df["longitude"] = df["longitude"] * 360 - 180

        # Export to parquet
        df.to_parquet(f"{folder}/part_{i}.parquet")


if __name__ == "__main__":

    for order, num_files in DATASETS:
        create_one_dataset(order, num_files)
