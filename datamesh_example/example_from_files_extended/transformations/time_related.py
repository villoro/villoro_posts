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


class AddLocalTime(Transformation):
    def transform(self, table: Table) -> Table:

        time_col = f"{table.creation_time}_local"
        time_of_day_condition = f"""CASE
            WHEN hour({time_col}) >= 0 AND hour({time_col}) <= 5 THEN 'Late'
            WHEN hour({time_col}) >= 6 AND hour({time_col}) <= 10 THEN 'Breakfast'
            WHEN hour({time_col}) >= 11 AND hour({time_col}) <= 16 THEN 'Lunch'
            WHEN hour({time_col}) >= 17 AND hour({time_col}) <= 23 THEN 'Dinner'
        END"""

        table.sdf = table.sdf.withColumn(
            time_col,
            F.from_utc_timestamp(table.creation_time, F.col(table.time_zone)),
        ).withColumn(table.time_of_day, F.expr(time_of_day_condition))

        return table
