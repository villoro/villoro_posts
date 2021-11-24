from datetime import date
from datetime import timedelta

from pyspark.sql import DataFrame

from loaders import LoaderCustomEvent
from writers import WriterCustomEvent


class CustomEventPort(LoaderCustomEvent, WriterCustomEvent):

    creation_date = "p_creation_date"
    city = "custom_attributes__city"

    def __init__(self, spark, exec_date: date, n_days: int):
        self.exec_date = exec_date
        self.n_days = n_days

        super().__init__(spark)

    def select(self, sdf) -> DataFrame:

        start = self.exec_date - timedelta(days=self.n_days)
        end = self.exec_date

        return sdf.filter(f"{self.creation_date} BETWEEN '{start:%Y-%m-%d}' AND '{end:%Y-%m-%d}'")


class OrderCreatedPort(CustomEventPort):
    name_in = "order_created"
    name_out = "order_created"
