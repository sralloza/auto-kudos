"""Exceptions used in the api."""


class StravaError(Exception):
    """Strava error."""


class CredentialsNotFoundError(StravaError):
    """Credentials not found error."""


class LoginError(StravaError):
    """Credentials are not valid."""
