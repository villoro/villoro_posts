from abc import ABC
from abc import abstractmethod


class Writer(ABC):
    @property
    @abstractmethod
    def database_out(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def name_out(self):
        raise NotImplementedError

    def write(self):
        self.sdf.write.format("parquet").saveAsTable(f"{self.database_out}.{self.name_out}")


class WriterCustomEvent(Writer):
    database_out = "enriched_custom_events"


class WriterScreenView(Writer):
    database_out = "enriched_screen_views"
