import pyspark.sql.functions as F

from transformations.interfaces import Table
from transformations.interfaces import Transformation

from ports.live_db import CitiesPort


class AddTimezone(Transformation):
    def __init__(self, cities: CitiesPort):
        self.cities = cities

    def transform(self, table: Table) -> Table:

        table.sdf = table.sdf.join(
            F.broadcast(self.cities.sdf),
            on=table.sdf[table.city] == self.cities.sdf[self.cities.code],
            how="left",
        ).drop(self.cities.code)

        return table
