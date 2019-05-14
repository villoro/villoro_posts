import yaml
import numpy as np
from numba import jit, njit
from tqdm import tqdm

from utils import timeit


def iter_and_sum(data):
    """ Sums each element in an iterable """
    out = 0
    for x in data:
        out += x

    return out


functions = [
    ("iter_and_sum", iter_and_sum),
    ("sum", sum),
    ("jit", jit(iter_and_sum)),
    ("njit", njit(iter_and_sum)),
    ("np.sum", np.sum),
]

tests = [(1000, 1e4), (200, 1e5), (100, 1e6), (20, 1e7), (10, 1e8), (5, 1e9)]


def test_all(functions=functions, tests=tests, tqdm_f=tqdm):
    """ Test all combinations """

    out = {}
    for iterations, size in tqdm_f(tests, desc="iterations"):

        size = int(size)

        m_list = np.random.choice(range(10), size=size)

        out[size] = {}
        for name, func in tqdm_f(functions, desc=str(size)):

            out[size][name] = timeit(iterations)(func)(m_list)

    with open("results.yaml", "w") as outfile:
        yaml.dump(out, outfile, default_flow_style=False)

    print("\nAll tests done")


if __name__ == "__main__":
    test_all()
