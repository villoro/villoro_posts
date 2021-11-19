from datetime import date

from ports.events import OrderCreatedPort
from ports.live_db import CitiesPort

from transformations.timezone import AddTimezone

from jobs.interfaces import TransformLinearly

from utils import get_spark_session


def do(spark, exec_date: date, n_days: int):
    order_created = OrderCreatedPort(spark, exec_date, n_days)
    transformations = [AddTimezone(CitiesPort(spark))]

    order_created_job = TransformLinearly(
        table=order_created,
        transformations=transformations,
    )
    order_created_job.run()


if __name__ == "__main__":
    spark = get_spark_session()
    do(spark, exec_date=date(2021, 11, 19), n_days=3)
