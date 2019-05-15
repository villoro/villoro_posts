import numpy as np
from numba import jit, njit
from tqdm import tqdm

from utils import timeit, store_results


def iter_and_sum(data):
    """ Sums each element in an iterable """
    out = 0
    for x in data:
        out += x

    return out


FUNCTIONS = [
    ("iter_and_sum", iter_and_sum),
    ("sum", sum),
    ("jit", jit(iter_and_sum)),
    ("njit", njit(iter_and_sum)),
    ("np.sum", np.sum),
]

TESTS = [
    (1000, 10_000),  # 1e4
    (200, 100_000),  # 1e5
    (100, 1_000_000),  # 1e6
    (20, 10_000_000),  # 1e7
    (10, 100_000_000),  # 1e8
    (5, 1_000_000_000),  # 1e9
]

test_name = "sum"


def test_all(tqdm_f=tqdm):
    """ Test all combinations """

    out = {}
    for iterations, size in tqdm_f(TESTS, desc="iterations"):

        size = int(size)

        m_list = np.random.choice(range(10), size=size)

        out[size] = {}
        for name, func in tqdm_f(FUNCTIONS, desc=str(size)):

            out[size][name] = timeit(iterations)(func)(m_list)

    store_results(out, test_name)


if __name__ == "__main__":
    test_all()
