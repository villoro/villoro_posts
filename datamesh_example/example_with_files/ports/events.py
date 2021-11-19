from abc import abstractmethod
from datetime import date
from datetime import timedelta

from pyspark.sql import DataFrame

from adapters.loaders import LoaderCustomEvent
from adapters.writers import WriterCustomEvent

from utils import log


class CustomEventPort(LoaderCustomEvent, WriterCustomEvent):

    creation_date = "p_creation_date"
    city = "custom_attributes__city"

    def __init__(self, spark, exec_date: date, n_days: int):
        self.exec_date = exec_date
        self.n_days = n_days

        super().__init__(spark)

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    def load(self) -> DataFrame:

        start = self.exec_date - timedelta(days=self.n_days)
        end = self.exec_date

        sdf = self.spark.table(f"{self.database_in}.{self.name}")
        return sdf.filter(f"{self.creation_date} BETWEEN '{start:%Y-%m-%d}' AND '{end:%Y-%m-%d}'")

    def write(self):
        table = f"{self.database_out}.{self.name}"
        log.info(f"Writting table '{table}'")

        self.sdf.write.format("parquet").saveAsTable(table)


class OrderCreatedPort(CustomEventPort):
    name = "order_created"
