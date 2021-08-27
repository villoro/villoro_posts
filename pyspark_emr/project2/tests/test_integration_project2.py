import pytest

from project2 import __version__


@pytest.mark.integration
def test_version():
    assert __version__ == "0.1.0"
