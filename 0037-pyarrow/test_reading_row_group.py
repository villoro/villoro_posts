from os import walk

from tqdm import tqdm
import pandas as pd
import pyarrow.dataset as ds
import pyarrow.parquet as pq

from create_datasets import PATH_PARQUET
from utils import store_results
from utils import timeit

TEST_NAME = "reading_rg"

PARTITION_COL = "creation_month"
FILTER_VAL = "2020-01"

ROWGROUP_COL = "state"
ROWGROUP_FILTER_VAL = "FL"

ITERATIONS = 20


def get_file_path(path):

    parquet_files = []
    for (dirpath, dirnames, filenames) in walk(path):
        for f in filenames:
            if f.endswith(".parquet"):
                parquet_files.append(f"{dirpath}/{f}")
    return parquet_files


def pyarrow_single_read(path):

    dfs = []
    for file in get_file_path(path):
        df = pq.read_table(file).to_pandas()
        dfs.append(df)
    df = pd.concat(dfs)

    df = df[(df[PARTITION_COL] >= FILTER_VAL) &
            (df[ROWGROUP_COL] == ROWGROUP_FILTER_VAL)]

    return df.shape


def pyarrow_parquet_ds_read(path):

    kwa = {"filters": [(f"p_{PARTITION_COL}", ">=", FILTER_VAL),
                       (f"{ROWGROUP_COL}", "=", ROWGROUP_FILTER_VAL)]}
    dataset = pq.ParquetDataset(path, validate_schema=False, **kwa)
    df = dataset.read_pandas().to_pandas()

    return df.shape


def pyarrow_ds_read(path):
    dataset = ds.dataset(path, format="parquet", partitioning="hive")
    table = dataset.to_table(filter=(ds.field(f"p_{PARTITION_COL}") >= FILTER_VAL) &
                                    (ds.field(ROWGROUP_COL) == ROWGROUP_FILTER_VAL))

    df = table.to_pandas(use_threads=True)
    return df.shape


FUNCTIONS = [
    pyarrow_single_read,
    pyarrow_parquet_ds_read,
    pyarrow_ds_read,
]


def test_all(tqdm_f=tqdm):
    """ Test all combinations """

    out = {}
    for i in range(1, 3):
        for func in tqdm_f(FUNCTIONS, desc=f"dataset_{i}"):
            out[f"{func.__name__}_{i}"] = timeit(ITERATIONS)(func)(f"{PATH_PARQUET}_{i}")

    store_results(out, TEST_NAME)


if __name__ == "__main__":
    test_all()
