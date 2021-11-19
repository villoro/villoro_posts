from datetime import date

import pandas as pd

from pyspark.sql import SparkSession

LIVE_DB = "standardized_glovo_live"
CUSTOM_EVENT_IN = "mpcustomer_custom_events"

DATABASES = [
    # Inputs
    LIVE_DB,
    CUSTOM_EVENT_IN,
    "mpcustomer_screen_views"
    # Outputs
    "enriched_custom_events",
    "enriched_screen_views",
]


def recreate_databases(spark):
    for db in DATABASES:
        spark.sql(f"DROP DATABASE IF EXISTS {db} CASCADE")
        spark.sql(f"CREATE DATABASE IF NOT EXISTS {db}")


DATA_CITIES = {
    "code": ["BCN", "VAL", "CAG"],
    "time_zone": ["Europe/Madrid", "Europe/Madrid", "Europe/Rome"],
    "country": ["ES", "ES", "IT"],
}

DATA_DEVICES = {
    "id": ["d1", "d2", "d3", "d4"],
    "experiment_score": [10, 30, 50, 99],
}

DATA_ORDER_CREATED = {
    "custom_attributes__city": ["BCN", "BCN", "CAG", "CAG"],
    "p_creation_date": [
        date(2021, 11, 19),
        date(2021, 11, 18),
        date(2021, 11, 17),
        date(2021, 11, 1),
    ],
}


def create_tables(spark):
    def create_table(data, database, table):
        dfg = pd.DataFrame(data)
        spark.createDataFrame(dfg).write.saveAsTable(f"{database}.{table}")

    create_table(DATA_CITIES, LIVE_DB, "cities")
    create_table(DATA_DEVICES, LIVE_DB, "devices")
    create_table(DATA_DEVICES, CUSTOM_EVENT_IN, "order_created")
