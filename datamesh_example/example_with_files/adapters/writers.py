from abc import ABC
from abc import abstractmethod


class Writer(ABC):
    @abstractmethod
    def write(self):
        raise NotImplementedError


class WriterCustomEvent(Writer):
    database_out = "enriched_custom_events"


class WriterScreenView(Writer):
    database_out = "enriched_screen_views"
