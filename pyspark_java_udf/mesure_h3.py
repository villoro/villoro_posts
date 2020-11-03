import h3

import pyspark.sql.functions as F
import pyspark.sql.types as T

from time import time
from tqdm import tqdm

from pyspark.sql import SparkSession

from py4j.java_gateway import java_import

from utils import store_results
from utils import timeit

spark = (
    SparkSession.builder.appName("test")
    .config("spark.sql.sources.partitionOverwriteMode", "static")
    .config("spark.sql.caseSensitive", "true")
    .config("spark.driver.extraJavaOptions", "-Duser.timezone=GMT")
    .config("spark.executor.extraJavaOptions", "-Duser.timezone=GMT")
    .config("spark.sql.session.timeZone", "UTC")
    .getOrCreate()
)


@F.udf(T.StringType())
def get_h8_py(lat, lon):
    if lat is not None and lon is not None:
        return h3.geo_to_h3(lat, lon, 8)


spark.udf.registerJavaFunction("get_h8_java", "get_h8", T.StringType())


def test_python(order):
    (
        spark.read.parquet(f"data/dataset_{order}")
        .withColumn("h8", get_h8_py("latitude", "longitude"))
        .write.parquet("data/output", mode="overwrite")
    )


def test_java(order):
    (
        spark.read.parquet(f"data/dataset_{order}")
        .withColumn("h8", F.expr("get_h8_java(latitude, longitude)"))
        .write.parquet("data/output", mode="overwrite")
    )


# fmt: off
TESTS = {
    "python": {
        "function": test_python,
        "tests": [
            (11, 3),
            (10, 4),
            (10, 5),
            (10, 6),
            (5, 7),
            (2, 8),
        ],
    },
    "java": {
        "function": test_java,
        "tests": [
            (11, 3),
            (10, 4),
            (10, 5),
            (10, 6),
            (5, 7),
            (2, 8),
        ],
    },
}
# fmt: on


def test_all():
    """ Test all combinations """

    for name, data in TESTS.items():

        print(f"\nTESTING '{name.upper()}'")
        func = data["function"]

        out = {}
        for n_iterations, order in data["tests"]:
            print(f"- Test order {order}")
            out[f"order_{order}"] = timeit(func, n_iterations=n_iterations, order=order)

        store_results(out, name)


if __name__ == "__main__":
    test_all()
