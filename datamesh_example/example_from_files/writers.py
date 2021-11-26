from abc import ABC
from abc import abstractmethod

from utils import log


class Writer(ABC):
    @property
    @abstractmethod
    def database_out(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def name_out(self):
        raise NotImplementedError

    @property
    def table_out(self):
        return f"{self.database_out}.{self.name_out}"

    def write(self):
        log.info(f"Writting '{self.table_out}'")
        self.sdf.repartition(1).write.format("parquet").saveAsTable(self.table_out)


class WriterCustomEvent(Writer):
    database_out = "enriched_custom_events"


class WriterScreenView(Writer):
    database_out = "enriched_screen_views"
