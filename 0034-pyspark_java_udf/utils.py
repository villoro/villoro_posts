"""
    Function to run n_times another function and output the execution times.

    It uses 'perf_counter' instead of 'time' since it has more precission
"""

from time import perf_counter

import yaml


def timeit(func, n_iterations=10, *args, **kwa):
    """ Outputs the execution time of a function """

    out = []
    for _ in range(n_iterations):
        t0 = perf_counter()
        result = func(*args, **kwa)
        out.append(perf_counter() - t0)
    return out


def store_results(data, test_name):
    """ Store results as a yaml """

    # If one test is not run, don't overwrite results
    if data:
        with open(f"results/{test_name}.yaml", "w") as outfile:
            yaml.dump(data, outfile, default_flow_style=False)

    print(f"\nAll tests done for {test_name}")
