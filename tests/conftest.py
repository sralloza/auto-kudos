from unittest import mock

import pytest


@pytest.fixture(autouse=True, scope="session")
def setup():
    mock.patch("requests.Session").start()
    yield
    mock.patch.stopall()
