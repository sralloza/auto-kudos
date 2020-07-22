"""Exceptions used in the api."""
import pytest

from strava_api.exceptions import CredentialsNotFoundError, LoginError, StravaError


class TestStravaError:
    def test_inheritance(self):
        assert issubclass(StravaError, Exception)

    def test_raises(self):
        with pytest.raises(StravaError):
            raise StravaError


class TestCredentialsNotFoundError:
    def test_inheritance(self):
        assert issubclass(CredentialsNotFoundError, StravaError)

    def test_raises(self):
        with pytest.raises(CredentialsNotFoundError):
            raise CredentialsNotFoundError


class TestLoginError:
    def test_inheritance(self):
        assert issubclass(LoginError, StravaError)

    def test_raises(self):
        with pytest.raises(LoginError):
            raise LoginError
