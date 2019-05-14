"""
    Timeit decorator.
    This decorator will run n_times a function and output the execution times.

    More info about decorators at: https://develop.villoro.com/post/decorators

    It uses 'perf_counter' instead of 'time' since it has more precission
"""

from time import perf_counter

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


def test_all(functions, tests, test_name="out", tqdm_f=tqdm):
    """ Test all combinations """

    out = {}
    for iterations, size in tqdm_f(tests, desc="iterations"):

        size = int(size)

        m_list = np.random.choice(range(10), size=size)

        out[size] = {}
        for name, func in tqdm_f(functions, desc=str(size)):

            out[size][name] = timeit(iterations)(func)(m_list)

    with open(f"results/{test_name}.yaml", "w") as outfile:
        yaml.dump(out, outfile, default_flow_style=False)

    print(f"\nAll tests done fro {test_name}")
