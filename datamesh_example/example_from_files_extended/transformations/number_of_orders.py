import pyspark.sql.functions as F

from transformations.interfaces import Table
from transformations.interfaces import Transformation

from ports.live_db import OrdersPort


class AddNumberOfOrders(Transformation):
    def __init__(self, orders: OrdersPort):
        self.orders = orders

    def transform(self, table: Table) -> Table:

        output_columns = table.sdf.columns + [self.orders.number_of_orders]

        orders_expression = (
            "IF({orders_time} IS NULL OR to_date({orders_time}) > to_date({sdf_time}), 0, 1)"
        ).format(orders_time=self.orders.creation_time, sdf_time=table.creation_time)

        sdf_temp = (
            table.sdf.select(table.customer_id, table.creation_time)
            .join(
                self.orders.sdf,
                on=table.customer_id,
                how="left",
            )
            .withColumn("orders", F.expr(orders_expression))
            .groupBy(table.customer_id)
            .agg(F.sum("orders").alias(self.orders.number_of_orders))
        )

        table.sdf = table.sdf.join(
            sdf_temp,
            on=table.customer_id,
            how="left",
        ).select(*output_columns)

        return table
