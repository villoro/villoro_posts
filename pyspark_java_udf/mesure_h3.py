import h3

import pyspark.sql.functions as F
import pyspark.sql.types as T

from time import time
from tqdm import tqdm

from pyspark.sql import SparkSession

from py4j.java_gateway import java_import

from utils import timeit

TESTS = [3, 4, 5]


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


FUNCTIONS = [("python", test_python), ("java", test_java)]


def test_all(tqdm_f=tqdm):
    """ Test all combinations """

    out = {}
    for order in tqdm_f(TESTS, desc="iterations"):

        out[order] = {}
        for name, func in tqdm_f(FUNCTIONS, desc=f"order_{order}"):

            out[order][name] = timeit(func, order=order)

    store_results(out, "h3")


if __name__ == "__main__":
    test_all()
