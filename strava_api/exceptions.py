"""Exceptions used in the api."""


class StravaError(Exception):
    """Strava error."""


class CredentialsNotFoundError(StravaError):
    """Credentials not found error."""
