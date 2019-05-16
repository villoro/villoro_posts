import numpy as np
import pandas as pd
from numba import jit, njit, vectorize, int32
from tqdm import tqdm

from utils import timeit, store_results


def prepare_dataset(size):
    """
        Create a dataset for the tests
        It will be a dataframe with two columns:
            date: with format YYYY-MM-DD
            time: with format hhmmsscc as integer
        Creating a big dataframe requires a lot of RAM.
        I was able to create a 10**7 dataset with my computer (16 GB RAM) but not the 10**8.
    """

    print(f"Creating dataset of order {int(np.log10(size))}")

    # Generate raw data
    data = {
        "year": np.random.choice([str(x) for x in range(2000, 2020)], size),
        "month": np.random.choice([str(x).zfill(2) for x in range(1, 12)], size),
        "day": np.random.choice([str(x).zfill(2) for x in range(1, 29)], size),
        "hour": np.random.choice(range(24), size),
        "minute": np.random.choice(range(60), size),
        "second": np.random.choice(range(60), size),
        "cent": np.random.choice(range(100), size),
    }

    # Create a dataframe
    df = pd.DataFrame(data.values(), index=data.keys()).T

    # Create 'date' and 'time' columns
    df["date"] = df["year"] + "-" + df["month"] + "-" + df["day"]
    df["time"] = df["cent"] + 100 * (df["second"] + 100 * (df["minute"] + 100 * df["hour"]))

    # drop used columns
    for col in data.keys():
        del df[col]

    return df


def zfill(df):
    """
        1. Transform time to str
        2. zfill
        3. split time as string lists
        4. pd.to_datetime
    """

    aux = df["time"].apply(str).apply(lambda x: x.zfill(8)).str
    return pd.to_datetime(
        df["date"] + " " + aux[:2] + ":" + aux[2:4] + ":" + aux[4:6] + "." + aux[6:]
    )


def fix_time_individual(df):
    """
        1. pandas.apply a jit function to add 0 to time
        2. concat date + time
        3. change to np.datetime64
    """

    @jit
    def _fix_time(x):
        aux = "0" * (8 - len(str(x))) + str(x)
        return aux[:2] + ":" + aux[2:4] + ":" + aux[4:6] + "." + aux[6:]

    return (df["date"] + " " + df["time"].apply(_fix_time)).astype(np.datetime64)


def fix_time_np_string(df):
    """
        1. Use a jit function to add 0 to each time
        2. concat date + time
        3. change to np.datetime64
    """

    @jit
    def _fix_time(mlist):

        out = np.empty(mlist.shape, dtype=np.object)

        for i in range(len(mlist)):

            elem = str(mlist[i])
            aux = "0" * (8 - len(elem)) + elem

            out[i] = aux[:2] + ":" + aux[2:4] + ":" + aux[4:6] + "." + aux[6:]

        return out

    return (df["date"].values + " " + _fix_time(df["time"].values)).astype(np.datetime64)


def fix_time_np_datetime(df):
    """
        1. Iterate time and date with jit function
        2. Transform each element to string and add 0s
        3. Split the string
        4. Cast each element to np.datetime64
    """

    @jit
    def _fix_date(mdate, mtime):

        out = np.empty(mtime.shape, dtype="datetime64[s]")

        for i in range(len(mtime)):

            elem = str(mtime[i])
            aux = "0" * (8 - len(elem)) + elem

            aux = mdate[i] + " " + aux[:2] + ":" + aux[2:4] + ":" + aux[4:6] + "." + aux[6:]

            out[i] = np.datetime64(aux)

        return out

    return _fix_date(df["date"].values, df["time"].values)


def np_divmod_jit(df):
    """
        1. Iterate time and date with jit function
        2. Use np.divmod to transfom HHMMSSCC to miliseconds integer
        3. Cast date as np.datetime and time to timedelta
        4. Sum date and time
    """

    @jit
    def _fix_date(mdate, mtime):

        time_out = np.empty(mtime.shape[0], dtype=np.int32)

        for i in range(mtime.shape[0]):
            aux, cent = np.divmod(mtime[i], 100)
            aux, seconds = np.divmod(aux, 100)
            hours, minutes = np.divmod(aux, 100)

            time_out[i] = 10 * (cent + 100 * (seconds + 60 * (minutes + 60 * hours)))

        return mdate.astype(np.datetime64) + time_out.astype("timedelta64[ms]")

    return _fix_date(df["date"].values, df["time"].values)


def divmod_njit(df):
    """
        1. Iterate time with njit function
        2. Use divmod to transfom HHMMSSCC to miliseconds integer
        3. Outside the njit function cast date as np.datetime and time to timedelta
        4. Sum date and time
    """

    @njit
    def _fix_time(mtime):

        time_out = np.empty(mtime.shape)

        for i in range(mtime.shape[0]):
            aux, cent = divmod(mtime[i], 100)
            aux, seconds = divmod(aux, 100)
            hours, minutes = divmod(aux, 100)

            time_out[i] = 10 * (cent + 100 * (seconds + 60 * (minutes + 60 * hours)))

        return time_out

    return df["date"].values.astype(np.datetime64) + _fix_time(
        df["time"].values.astype(np.int32)
    ).astype("timedelta64[ms]")


def divmod_vectorize(df):
    """
        1. Use divmod to transfom HHMMSSCC to miliseconds integer with vectorize
        2. Outside the njit function cast date as np.datetime and time to timedelta
        3. Sum date and time
    """

    @vectorize([int32(int32)])
    def _fix_time(mtime):

        aux, cent = divmod(mtime, 100)
        aux, seconds = divmod(aux, 100)
        hours, minutes = divmod(aux, 100)

        return 10 * (cent + 100 * (seconds + 60 * (minutes + 60 * hours)))

    return df["date"].values.astype(np.datetime64) + _fix_time(
        df["time"].values.astype(np.int32)
    ).astype("timedelta64[ms]")


FUNCTIONS = [
    zfill,
    fix_time_individual,
    fix_time_np_string,
    fix_time_np_datetime,
    np_divmod_jit,
    divmod_njit,
    divmod_vectorize,
]

TESTS = [
    (100, 100),  # 1e2
    (100, 1_000),  # 1e3
    (100, 10_000),  # 1e4
    (50, 100_000),  # 1e5
    (20, 1_000_000),  # 1e6
    (10, 10_000_000),  # 1e7
    (5, 100_000_000),  # 1e8
]

TEST_NAME = "fix_datetime"


def test_all(tqdm_f=tqdm):
    """ Test all combinations """

    # Create dataframe with max test size.
    # It will be sliced at each test instead of being created n times
    df = prepare_dataset(max([x for _, x in TESTS]))

    out = {}
    for iterations, size in tqdm_f(TESTS, desc="iterations"):

        out[size] = {}
        for func in tqdm_f(FUNCTIONS, desc=f"o:{int(np.log10(size))} i:{iterations}"):

            out[size][func.__name__] = timeit(iterations)(func)(df.head(size))

    store_results(out, TEST_NAME)


if __name__ == "__main__":
    test_all()
