from datetime import datetime

from pyspark.sql import DataFrame

from adapters.loaders import LoaderLiveDB


class CitiesPort(LoaderLiveDB):
    name_in = "cities"

    code = "code"
    time_zone = "time_zone"
    country_code = "country_code"

    def select(self, sdf) -> DataFrame:
        return sdf.select(self.code, self.time_zone, self.country_code)


class DevicesPort(LoaderLiveDB):
    name_in = "devices"

    device_id = "custom_attributes__device_id"
    experiment_score = "device_experiment_score"

    def select(self, sdf) -> DataFrame:
        return sdf.selectExpr(
            f"id AS {self.device_id}",
            f"experiment_score AS {self.experiment_score}",
        )


class CustomersPort(LoaderLiveDB):
    name_in = "customers"

    customer_id = "customer_id"
    experiment_score = "customer_experiment_score"

    def select(self, sdf) -> DataFrame:
        return sdf.selectExpr(
            self.customer_id,
            f"experiment_score AS {self.experiment_score}",
        )


class OrdersPort(LoaderLiveDB):
    name_in = "orders"

    customer_id = "customer_id"
    creation_time = "order_creation_time"

    def select(self, sdf) -> DataFrame:
        return sdf.selectExpr(
            self.customer_id,
            f"creation_time AS {self.order_creation_time}",
        )


class CustomerSubscriptionsPort(LoaderLiveDB):
    id = "customer_subscription_id"
    start_date = "start_date"
    expiration_date = "expiration_date"
    customer_id = "s_customer_id"

    def __init__(self, spark, exec_date: date, n_days: int):
        self.exec_date = exec_date
        self.n_days = n_days

        super().__init__(spark)

    def load(self) -> DataFrame:

        start = self.exec_date - timedelta(days=self.number_of_days)

        query = f"""
            SELECT
                csp.customer_subscription_id AS {self.id},
                cs.customer_id as {self.customer_id},
                csp.{start_date},
                csp.{expiration_date}
            FROM {self.database_in}.customer_subscription_periods AS csp
            LEFT JOIN {self.database_in}.customer_subscriptions   AS cs
                ON csp.customer_subscription_id = cs.id
            WHERE csp.expiration_date >= '{start:%Y-%m-%d}'
        """

        return self.spark.sql(query)
