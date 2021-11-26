from typing import List

from transformations.interfaces import Table
from transformations.interfaces import Transformation


class TransformLinearlyJob:
    def __init__(self, table: Table, transformations: List[Transformation]):
        self.table = table
        self.transformations = transformations

    def run(self):
        for transformation in self.transformations:
            self.table = transformation._apply(self.table)

        self.table.write()
