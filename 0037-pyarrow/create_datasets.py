import os
import pandas as pd

from tqdm import tqdm

PATH_CSV = "data/US_Accidents_Dec20_Updated.csv"
PATH_PARQUET_0 = "data/accidents_0.parquet"
PATH_PARQUET_1 = "data/accidents_1"
PATH_PARQUET_2 = "data/accidents_2"


def transform_to_parquet():
    """ Read the csv and export it as a parquet file """

    print("Reading data")

    df = pd.read_csv(PATH_CSV, index_col=0, parse_dates=True)
    df.columns = [x.lower() for x in df.columns]

    # Using 'datetime64[s]' since we don't need to much precision
    # Also it avoids problems with parquet

    for x in ["start_time", "end_time", "weather_timestamp"]:
        df[x] = pd.to_datetime(df[x]).astype("datetime64[s]")

    # Add partition column
    df["p_creation_month"] = df["start_time"].to_numpy().astype("datetime64[M]")

    print("Exporting 1/3")

    df.to_parquet(PATH_PARQUET_0)

    return df


def export_one_file_per_partition(df_in):
    """ Create one file per partition """

    for month, df in tqdm(df_in.groupby("p_creation_month"), desc="Export 2/3"):
        # Create the folder
        path = f"{PATH_PARQUET_1}/p_creation_month={month:%Y-%m}"
        os.makedirs(path, exist_ok=True)

        df.to_parquet(f"{path}/0001.parquet")


def export_multiple_files_per_partition(df_in):
    """ Create one file per partition """

    for month, df in tqdm(df_in.groupby("p_creation_month"), desc="Export 3/3"):
        # Create the folder
        path = f"{PATH_PARQUET_2}/p_creation_month={month:%Y-%m}"
        os.makedirs(path, exist_ok=True)

        for i, (_, df_out) in enumerate(df.groupby("state")):
            df_out.to_parquet(f"{path}/{str(i).zfill(4)}.parquet")


if __name__ == "__main__":

    df = transform_to_parquet()
    export_one_file_per_partition(df)
    export_multiple_files_per_partition(df)

    print("All extractions done")
