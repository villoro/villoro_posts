from abc import abstractmethod
from datetime import date


from ports.events import OrderCreatedPort
from ports.live_db import CitiesPort
from ports.live_db import CustomerSubscriptionsPort
from ports.live_db import OrdersPort

from transformations.number_of_orders import AddNumberOfOrders
from transformations.prime_data import AddIsPrime
from transformations.time_related import AddLocalTime
from transformations.time_related import AddTimezone

from jobs.interfaces import TransformLinearlyJob

from utils import get_spark_session


class EnrichActionJob(TransformLinearlyJob):
    def __init__(self, spark, exec_date, n_days):
        self.spark = spark
        self.exec_date = exec_date
        self.n_days = n_days

        # Create the table
        self.table = self.action_port(spark, exec_date, n_days)

        # Set transformations
        self.transformations = [
            AddTimezone(CitiesPort(spark)),
            AddLocalTime(),
            AddNumberOfOrders(OrdersPort(spark)),
            AddIsPrime(CustomerSubscriptionsPort(spark, exec_date=exec_date, n_days=n_days)),
        ]

    @property
    @abstractmethod
    def action_port(self):
        raise NotImplementedError


class EnrichCEOrderCreatedJob(EnrichActionJob):
    action_port = OrderCreatedPort
