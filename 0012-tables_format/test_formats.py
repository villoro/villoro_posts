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

COMPRESSIONS = {
    "csv": {
        "param_name": "compression",
        "read_with_param": True,
        "list": ["infer", "gzip", "bz2", "zip", "xz", None],
    },
    "pickle": {
        "param_name": "compression",
        "read_with_param": True,
        "list": ["infer", "gzip", "bz2", "zip", "xz", None],
    },
    "parquet": {
        "param_name": "compression",
        "read_with_param": False,  # Read function don't use compression param
        "list": ["snappy", "gzip", "brotli", None],
    },
    "msgpack": {
        "param_name": "compress",
        "read_with_param": False,  # Read function don't use compression param
        "list": ["zlib", "blosc", None],
    },
}


def clean():
    """ Clean previously created files """
    for name in os.listdir(PATH_DATA):
        if "." in name and name.split(".")[0] == "data":
            os.remove(f"{PATH_DATA}{name}")


def iterate_one_test(iterations, extension, func, args, kwargs):
    """
        Do some iterations for some function

        Args:
            size:       size of the file to test (0: small, 1: mediumn, 2: big)
            iterations: number of times to run the test
            func:       function to test
            args:       arguments for that function
            kwargs:     extra keyworded arguments
    """

    out = []

    for _ in tqdm(range(iterations), desc=f"- {extension:8}", leave=True):
        try:
            t0 = time()
            func(*args, **kwargs)

            # Store time
            out.append(time() - t0)

        except Exception as e:
            print(f"- Error with {extension}: {e}")

    return out


def test_write(size, iterations, exclude_formats, test_compress):
    """
        Test writting for one file

        Args:
            size:               size of the file to test (0: small, 1: mediumn, 2: big)
            iterations:         number of times to run the test
            exclude_formats:    formats to exclude in this test
            test_compress:      if True it will try all compressions

        Returns:
            dictionary with out
    """

    out = {}

    df = pd.read_csv(f"{PATH_DATA}{FILES[size]}.csv")

    for extension, func in tqdm(FUNCS["write"].items(), desc=f"{'write':10}", leave=True):

        # Skip this extension
        if extension in exclude_formats:
            continue

        if not test_compress or extension not in COMPRESSIONS:
            args = [df, f"{PATH_DATA}data.{extension}"]
            out[extension] = iterate_one_test(iterations, extension, func, args, {})

        # Try all compressions
        else:

            if extension not in COMPRESSIONS:
                continue

            # Get name of compression parameter and list of extensions
            comp_list = COMPRESSIONS[extension]["list"]
            comp_param_name = COMPRESSIONS[extension]["param_name"]

            for comp in tqdm(comp_list, desc=f"{extension:10}", leave=True):
                name = f"{extension}_{str(comp)}"
                out[name] = iterate_one_test(
                    iterations,
                    extension=name,
                    func=func,
                    args=[df, f"{PATH_DATA}data.{extension}_{comp}"],
                    kwargs={comp_param_name: comp},
                )

    return out


def test_read(size, iterations, exclude_formats, test_compress):
    """
        Test read for one file

        Args:
            size:               size of the file to test (0: small, 1: mediumn, 2: big)
            iterations:         number of times to run the test
            exclude_formats:    formats to exclude in this test
            test_compress:      if True it will try all compressions

        Returns:
            dictionary with out
    """

    out = {}

    for extension, func in tqdm(FUNCS["read"].items(), desc=f"{'read':10}", leave=True):

        # Skip this extension
        if extension in exclude_formats:
            continue

        if not test_compress or extension not in COMPRESSIONS:
            args = [f"{PATH_DATA}data.{extension}"]
            out[extension] = iterate_one_test(iterations, extension, func, args, {})

        # Try all compressions
        else:

            if extension not in COMPRESSIONS:
                continue

            # Get name of compression parameter and list of extensions
            comp_list = COMPRESSIONS[extension]["list"]
            comp_param_name = COMPRESSIONS[extension]["param_name"]
            use_param = COMPRESSIONS[extension]["read_with_param"]

            for comp in tqdm(comp_list, desc=f"{extension:10}", leave=True):
                name = f"{extension}_{str(comp)}"
                out[name] = iterate_one_test(
                    iterations,
                    extension=name,
                    func=func,
                    args=[f"{PATH_DATA}data.{extension}_{comp}"],
                    kwargs={comp_param_name: comp} if use_param else {},
                )
    return out


def store_results(data, size, iterations):
    """ Store results as a yaml """

    with open(f"{PATH_RESULTS}results_s{size}_i{iterations}.yaml", "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

    print(f"\n- Data {PATH_RESULTS}results_s{size}_i{iterations}.yaml stored")


def full_test(size, iterations=10, exclude_formats=[], test_compress=False):
    """ Do both tests and store the results"""

    clean()

    print(f"\nFULL TEST. size: {size}, iterations: {iterations}")
    out = {
        "write": test_write(size, iterations, exclude_formats, test_compress),
        "read": test_read(size, iterations, exclude_formats, test_compress),
    }

    # Also get file sizes
    out["file_size"] = {}

    for file in os.listdir(PATH_DATA):
        name, extension = file.split(".")

        if name == "data":
            out["file_size"][extension] = os.path.getsize(f"{PATH_DATA}{file}")

    store_results(out, size, iterations)


def test_1():
    """ Runs some tests with all extensions and exclude big dataframe """

    full_test(0, iterations=100)
    full_test(1, iterations=10)


def test_2():
    """ Run tests trying all compressions without xlsx extension """

    full_test(1, iterations=5, exclude_formats=["xlsx"], test_compress=True)


def test_3():
    """ Run test with the big dataframe and trying the compressions """

    full_test(2, iterations=1, exclude_formats=["xlsx", "csv"], test_compress=True)


if __name__ == "__main__":

    # Dummy test
    # full_test(0, iterations=20, exclude_formats=["xlsx"], test_compress=True)

    # test_1()
    # test_2()
    test_3()
