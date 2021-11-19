from abc import ABC
from abc import abstractmethod

from pyspark.sql import DataFrame

from utils import log


class Transformation(ABC):
    def _apply(self, sdf: DataFrame) -> DataFrame:
        """This shouldn't be implemented"""

        log.info(f"Applying transformation '{self.__name__}'")
        return self.transform(sdf)

    @abstractmethod
    def transform(self, sdf: DataFrame) -> DataFrame:
        raise NotImplementedError


class Table(ABC):
    @abstractmethod
    def sdf(self):
        raise NotImplementedError
