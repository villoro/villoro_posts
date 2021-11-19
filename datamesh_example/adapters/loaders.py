from abc import ABC
from abc import abstractmethod

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession


class Loader(ABC):
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.sdf = self.load()

    @abstractmethod
    def load(self) -> DataFrame:
        raise NotImplementedError


class LoaderLiveDB(Loader):
    database_in = "standardized_glovo_live"


class LoaderCustomEvent(Loader):
    database_in = "mpcustomer_custom_events"


class LoaderScreenView(Loader):
    database_in = "mpcustomer_screen_views"
