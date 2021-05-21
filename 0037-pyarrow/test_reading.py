from os import walk
from tqdm import tqdm

import pandas as pd
import pyarrow.dataset as ds
import pyarrow.parquet as pq

from create_datasets import PATH_PARQUET
from utils import store_results
from utils import timeit

TEST_NAME = "reading"

PARTITION_COL = "p_creation_month"
FILTER_VAL = "2020-12"

ITERATIONS = 1


def get_file_path(path):

    parquet_files = []
    for (dirpath, dirnames, filenames) in walk(path):
        for f in filenames:
            if f.endswith(".parquet"):
                parquet_files.append(f"{dirpath}/{f}")
    return parquet_files


def pandas_read(path, p_filter=False):

    dfs = []
    for file in get_file_path(path):
        df = pd.read_parquet(file)
        dfs.append(df)
    df = pd.concat(dfs)

    if p_filter:
        df = df[df[PARTITION_COL] >= FILTER_VAL]

    return df.shape


def pyarrow_single_read(path, p_filter=False):

    dfs = []
    for file in get_file_path(path):
        df = pq.read_table(file).to_pandas()
        dfs.append(df)
    df = pd.concat(dfs)
    if p_filter:
        df = df[df[PARTITION_COL] >= FILTER_VAL]

    return df.shape


def pyarrow_parquet_ds_read(path, p_filter=False):

    kwa = {"filters": [(PARTITION_COL, ">=", FILTER_VAL)]} if p_filter else {}
    dataset = pq.ParquetDataset(path, validate_schema=False, **kwa)
    df = dataset.read_pandas().to_pandas()

    return df.shape


def pyarrow_ds_read(path, p_filter=False):

    dataset = ds.dataset(path, format="parquet", partitioning="hive")
    if p_filter:
        df = dataset.to_table(filter=ds.field(PARTITION_COL) >= FILTER_VAL)
    else:
        df = dataset.to_table().to_pandas()

    return df.shape


FUNCTIONS = [
    pandas_read,
    pyarrow_single_read,
    pyarrow_parquet_ds_read,
    pyarrow_ds_read,
]


def test_all(tqdm_f=tqdm):
    """ Test all combinations """

    out = {}
    for i in range(3):
        for func in tqdm_f(FUNCTIONS, desc=f"dataset_{i}"):
            out[f"{func.__name__}_{i}"] = timeit(ITERATIONS)(func)(f"{PATH_PARQUET}_{i}")

    store_results(out, TEST_NAME)


if __name__ == "__main__":
    test_all()
