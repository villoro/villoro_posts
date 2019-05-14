import yaml
import numpy as np
from numba import jit, njit
from tqdm import tqdm

from utils import test_all


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

test_name = "sum"


if __name__ == "__main__":
    test_all(functions=functions, tests=tests, test_name=test_name)
