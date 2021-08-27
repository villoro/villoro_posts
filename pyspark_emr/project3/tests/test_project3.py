from project3 import __version__


def test_version():
    assert __version__ == "0.1.0"


def test_spark_app_name(spark):
    assert spark["appName"] == "test"


def test_spark_version(spark):
    assert spark["project.version"] == __version__
