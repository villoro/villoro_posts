from pyspark.sql import DataFrame

from adapters.loaders import LoaderLiveDB


class CitiesPort(LoaderLiveDB):
    code = "code"
    time_zone = "time_zone"
    country_code = "country_code"

    def load(self) -> DataFrame:
        sdf = self.spark.table(f"{self.database_in}.cities")
        return sdf.select(self.code, self.time_zone, self.country_code)


class DevicesPort(LoaderLiveDB):
    device_id = "custom_attributes__device_id"
    experiment_score = "device_experiment_score"

    def load(self) -> DataFrame:
        sdf = self.spark.table(f"{self.database_in}.devices")
        return sdf.selectExpr(
            f"id AS {self.device_id}",
            f"experiment_score AS {self.experiment_score}",
        )
