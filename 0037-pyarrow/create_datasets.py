import os
import pandas as pd

from loguru import logger as log
from tqdm import tqdm

PATH_CSV = "data/US_Accidents_Dec20_Updated.csv"
PATH_PARQUET = "data/accidents"


def transform_to_parquet():
    """ Read the csv and export it as a parquet file """

    log.info("Reading data")

    df = pd.read_csv(PATH_CSV, index_col=0, parse_dates=True)
    df.columns = [x.lower() for x in df.columns]

    # Using 'datetime64[s]' since we don't need to much precision
    # Also it avoids problems with parquet

    for x in ["start_time", "end_time", "weather_timestamp"]:
        df[x] = pd.to_datetime(df[x]).astype("datetime64[s]")

    # Add partition column
    df["creation_month"] = df["start_time"].to_numpy().astype("datetime64[M]")

    # Drop unuseful column that can give problems at reading (nullabe vs no nullable)
    df = df.drop(columns=["weather_condition"])

    path = f"{PATH_PARQUET}_0"
    os.makedirs(path, exist_ok=True)

    log.info("Exporting 1/3")
    df.to_parquet(f"{path}/0001.parquet")

    return df


def export_one_file_per_partition(df_in):
    """ Create one file per partition """

    log.info("Exporting 2/3")

    for month, df in tqdm(df_in.groupby("creation_month")):
        # Create the folder
        path = f"{PATH_PARQUET}_1/p_creation_month={month:%Y-%m}"
        os.makedirs(path, exist_ok=True)

        df.to_parquet(f"{path}/0001.parquet")


def export_multiple_files_per_partition(df_in):
    """ Create one file per partition """

    log.info("Exporting 3/3")

    for month, df in tqdm(df_in.groupby("creation_month")):
        # Create the folder
        path = f"{PATH_PARQUET}_2/p_creation_month={month:%Y-%m}"
        os.makedirs(path, exist_ok=True)

        for i, (_, df_out) in enumerate(df.groupby("state")):
            df_out.to_parquet(f"{path}/{str(i).zfill(4)}.parquet")


if __name__ == "__main__":

    df = transform_to_parquet()
    export_one_file_per_partition(df)
    export_multiple_files_per_partition(df)

    log.info("All extractions done")
