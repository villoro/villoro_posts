import pyspark.sql.functions as F

from transformations.interfaces import Table
from transformations.interfaces import Transformation

from ports.live_db import CustomerSubscriptionsPort


class AddIsPrime(Transformation):
    def __init__(self, customer_subscriptions: CustomerSubscriptionsPort):
        self.customer_subscriptions = customer_subscriptions

    def transform(self, table: Table) -> Table:

        subs = self.customer_subscriptions

        drop_cols = [
            subs.customer_id,
            subs.id,
            subs.start_date,
            subs.expiration_date,
        ]

        cond = [
            table.sdf[table.customer_id] == subs.sdf[subs.customer_id],
            table.sdf[table.creation_time].between(
                subs.sdf[subs.start_date],
                subs.sdf[subs.expiration_date],
            ),
        ]

        table.sdf = table.sdf.join(subs.sdf, on=cond, how="left").select(
            *[x for x in table.sdf.columns if x not in drop_cols],
            F.expr(f"IF({subs.id} IS NOT NULL, true, false)").alias(table.is_prime),
        )

        return table
