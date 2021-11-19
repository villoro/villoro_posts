from loguru import logger as log

from pyspark.sql import SparkSession


def get_spark_session():
    log.info("Creating Spark Session")
    return SparkSession.builder.appName("DM").getOrCreate()
