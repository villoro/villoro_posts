"""
    Timeit decorator.
    This decorator will run n_times a function and output the execution times.

    More info about decorators at: https://develop.villoro.com/post/decorators

    It uses 'perf_counter' instead of 'time' since it has more precission
"""

from time import perf_counter

import yaml
from tqdm import tqdm


def timeit(n_iterations=10):
    """ Allows to time a function n times """

    def timeit_decorator(func):
        """ Timing decorator """

        def timed_execution(*args):
            """ Outputs the execution time of a function """

            out = []
            for _ in range(n_iterations):
                t0 = perf_counter()
                result = func(*args)
                out.append(perf_counter() - t0)
            return out

        return timed_execution

    return timeit_decorator


def store_results(data, test_name):
    """ Store results as a yaml """

    with open(f"results/{test_name}.yaml", "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

    print(f"\nAll tests done for {test_name}")
