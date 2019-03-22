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

PATH = "data/"
FILES = ["bike_sharing_daily", "cbg_patterns", "checkouts-by-title"]

FUNCS = {
    "read": {"csv": pd.read_csv, "xlsx": pd.read_excel, "pickle": pd.read_pickle},
    "write": {
        "csv": pd.DataFrame.to_csv,
        "xlsx": pd.DataFrame.to_excel,
        "pickle": pd.DataFrame.to_pickle,
    },
}

ITERATIONS = {0: 10, 1: 2}  # 10, 2: 4}


def clean():
    """ Clean previously created files """
    for name in os.listdir(PATH):
        if "." in name and name.split(".")[0] == "data":
            os.remove(f"{PATH}{name}")


def test_write(size, iterations=10):
    """
        Test writting for one file

        Args:
            size:       size of the file to test (0: small, 1: mediumn, 2: big)
            iterations: number of times to run the test

        Returns:
            dictionary with results
    """

    df = pd.read_csv(f"{PATH}{FILES[size]}.csv")

    results = {}

    for extension, func in tqdm(FUNCS["write"].items(), desc=f"{'write':10}"):

        results[extension] = []

        for _ in tqdm(range(iterations), f"{extension:10}"):
            t0 = time()
            func(df, f"{PATH}data.{extension}")
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

    for extension, func in tqdm(FUNCS["read"].items(), desc=f"{'read':10}"):

        results[extension] = []

        for _ in tqdm(range(iterations), f"{extension:10}"):
            t0 = time()
            func(f"{PATH}data.{extension}")
            results[extension].append(time() - t0)

    return results


def store_results(data, size):
    """ Store results as a yaml """

    with open(f"{PATH}results_{size}.yaml", "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

    print(f"\n- Data {PATH}results_{size}.yaml stored")


def full_test(size, iterations=10):
    """ Do both tests and store the results"""

    clean()

    print(f"\nFULL TEST {size}")
    out = {"write": test_write(size, iterations), "read": test_read(size, iterations)}

    store_results(out, size)


if __name__ == "__main__":

    # full_test(0)

    for size, iterations in ITERATIONS.items():
        full_test(size, iterations)
