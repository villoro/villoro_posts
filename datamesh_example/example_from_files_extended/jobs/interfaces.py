from abc import abstractmethod
from datetime import date


class TransformLinearlyJob:
    def __init__(self, spark, exec_date: date, n_days: int):
        self.spark = spark
        self.exec_date = exec_date
        self.n_days = n_days

        # Create the table
        self.table = self.main_port(spark, exec_date, n_days)

        # Set transformations
        self.transformations = self.get_transformations()

    def run(self):
        for transformation in self.transformations:
            self.table = transformation._apply(self.table)

        self.table.write()

    @abstractmethod
    def get_transformations(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def main_port(self):
        raise NotImplementedError
