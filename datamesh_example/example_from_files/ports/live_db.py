from pyspark.sql import DataFrame

from loaders import LoaderLiveDB


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
