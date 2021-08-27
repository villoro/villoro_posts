import pytest

from project3 import __version__


@pytest.fixture(scope="session", autouse=True)
def spark():

    dummy_spark_session = {
        "appName": "test",
        "project.version": __version__,
        "spark.driver.extraJavaOptions": "-Duser.timezone=GMT",
    }
    return dummy_spark_session
