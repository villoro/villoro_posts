import shutil

from datetime import date
from datetime import datetime

import pandas as pd

from loguru import logger as log
from pyspark.sql import SparkSession

SPARK_WAREHOUSE_PATH = "spark-warehouse"

LIVE_DB = "standardized_glovo_live"
CUSTOM_EVENT_IN = "mpcustomer_custom_events"

DATABASES = [
    # Inputs
    LIVE_DB,
    CUSTOM_EVENT_IN,
    "mpcustomer_screen_views",
    # Outputs
    "enriched_custom_events",
    "enriched_screen_views",
]


def recreate_databases(spark):

    log.info(f"Removing spark warehouse (path = '{SPARK_WAREHOUSE_PATH}')")
    shutil.rmtree(SPARK_WAREHOUSE_PATH, ignore_errors=True)

    for db in DATABASES:
        log.info(f"Creating database '{db}'")
        spark.sql(f"DROP DATABASE IF EXISTS {db} CASCADE")
        spark.sql(f"CREATE DATABASE IF NOT EXISTS {db}")


DATA_CITIES = {
    "code": ["BCN", "VAL", "CAG"],
    "time_zone": ["Europe/Madrid", "Europe/Madrid", "Europe/Rome"],
    "country_code": ["ES", "ES", "IT"],
}

DATA_DEVICES = {
    "id": ["d1", "d2", "d3", "d4"],
    "experiment_score": [10, 30, 50, 99],
}

DATA_ORDERS = {
    "customer_id": [1, 1, 2],
    "creation_time": [
        datetime(2021, 11, 1),
        datetime(2021, 11, 30),
        datetime(2021, 11, 1),
    ],
}

DATA_ORDER_CREATED = {
    "custom_attributes__city": ["BCN", "BCN", "CAG", "CAG"],
    "customer_id": [1, 1, 2, 2],
    "creation_time": [
        datetime(2021, 11, 19, 12),
        datetime(2021, 11, 18, 8),
        datetime(2021, 11, 17, 5, 5),
        datetime(2021, 11, 1, 7, 29),
    ],
    "p_creation_date": [
        date(2021, 11, 19),
        date(2021, 11, 18),
        date(2021, 11, 17),
        date(2021, 11, 1),
    ],
}


def create_tables(spark):
    def create_table(data, database, table_name):
        table = f"{database}.{table_name}"

        log.info(f"Creating table '{table}'")
        dfg = pd.DataFrame(data)
        spark.createDataFrame(dfg).write.saveAsTable(table)

    create_table(DATA_CITIES, LIVE_DB, "cities")
    create_table(DATA_DEVICES, LIVE_DB, "devices")
    create_table(DATA_ORDERS, LIVE_DB, "orders")
    create_table(DATA_ORDER_CREATED, CUSTOM_EVENT_IN, "order_created")
