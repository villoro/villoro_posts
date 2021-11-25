from abc import ABC
from abc import abstractmethod

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession

from utils import log


class Loader(ABC):
    def __init__(self, spark: SparkSession, **kwargs):
        self.spark = spark
        self._set_kwargs(kwargs)

        # Needs to happen after setting kwargs
        self.sdf = self.load()

    def _set_kwargs(self, kwargs):
        """
        Set everything that comes in kwargs as a class attribute
            for example if we have kwargs = {n_days: 3}
            this is equivalent to self.n_days = 3
        """
        if "sdf" in kwargs.keys():
            raise ValueError(
                "You cannot pass 'sdf' as a parameter to the load "
                "since it needs to be use for the spark DataFrame"
            )

        self.__dict__.update(kwargs)

    @property
    @abstractmethod
    def database_in(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def name_in(self):
        raise NotImplementedError

    @property
    def table_in(self):
        return f"{self.database_in}.{self.name_in}"

    def load(self) -> DataFrame:
        log.info(f"Loading '{self.table_in}'")

        sdf = self.spark.table(self.table_in)
        return self.select(sdf)

    def select(self, sdf):
        raise NotImplementedError


class LoaderLiveDB(Loader):
    database_in = "standardized_glovo_live"


class LoaderCustomEvent(Loader):
    database_in = "mpcustomer_custom_events"


class LoaderScreenView(Loader):
    database_in = "mpcustomer_screen_views"
