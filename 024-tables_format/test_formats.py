"""
    Test different file formats for storing tables.

    There are 3 files with different sizes:
        small:  bike_sharing_daily (64 KB)
        medium: cbg_patterns (233 MB)
        big:    checkouts-by-title (6,62 GB)
"""

import os
from time import time

import yaml
import pandas as pd
from tqdm import tqdm

PATH_DATA = "data/"
PATH_RESULTS = "results/"

FILES = ["bike_sharing_daily", "cbg_patterns", "checkouts-by-title"]

FUNCS = {
    "read": {
        "csv": pd.read_csv,
        "xlsx": pd.read_excel,
        "pickle": pd.read_pickle,
        "feather": pd.read_feather,
        "parquet": pd.read_parquet,
        "msgpack": pd.read_msgpack,
    },
    "write": {
        "csv": pd.DataFrame.to_csv,
        "xlsx": pd.DataFrame.to_excel,
        "pickle": pd.DataFrame.to_pickle,
        "feather": pd.DataFrame.to_feather,
        "parquet": pd.DataFrame.to_parquet,
        "msgpack": pd.DataFrame.to_msgpack,
    },
}

# ITERATIONS = [10, 1]
ITERATIONS = [100, 10, 1]


def clean():
    """ Clean previously created files """
    for name in os.listdir(PATH_DATA):
        if "." in name and name.split(".")[0] == "data":
            os.remove(f"{PATH_DATA}{name}")


def test_write(size, iterations=10):
    """
        Test writting for one file

        Args:
            size:       size of the file to test (0: small, 1: mediumn, 2: big)
            iterations: number of times to run the test

        Returns:
            dictionary with results
    """

    df = pd.read_csv(f"{PATH_DATA}{FILES[size]}.csv")

    results = {}

    for extension, func in tqdm(FUNCS["write"].items(), desc=f"{'write':10}", leave=True):

        results[extension] = []

        for _ in tqdm(range(iterations), desc=f"- {extension:8}", leave=True):
            t0 = time()
            func(df, f"{PATH_DATA}data.{extension}")
            results[extension].append(time() - t0)

    return results


def test_read(size, iterations=10):
    """
        Test read for one file

        Args:
            size:       size of the file to test (0: small, 1: mediumn, 2: big)
            iterations: number of times to run the test

        Returns:
            dictionary with results
    """

    results = {}

    for extension, func in tqdm(FUNCS["read"].items(), desc=f"{'read':10}", leave=True):

        results[extension] = []

        for _ in tqdm(range(iterations), desc=f"- {extension:8}", leave=True):
            t0 = time()
            func(f"{PATH_DATA}data.{extension}")
            results[extension].append(time() - t0)

    return results


def store_results(data, size):
    """ Store results as a yaml """

    with open(f"{PATH_RESULTS}results_{size}.yaml", "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

    print(f"\n- Data {PATH_RESULTS}results_{size}.yaml stored")


def full_test(size, iterations=10):
    """ Do both tests and store the results"""

    clean()

    print(f"\nFULL TEST {size}")
    out = {"write": test_write(size, iterations), "read": test_read(size, iterations)}

    # Also get file sizes
    out["file_size"] = {x: os.path.getsize(f"{PATH_DATA}data.{x}") for x in FUNCS["read"].keys()}

    store_results(out, size)


if __name__ == "__main__":

    # full_test(0)

    for size, iterations in enumerate(ITERATIONS):
        full_test(size, iterations)
