"""Manages credentials of the api."""

from logging import getLogger
from os import environ
from pathlib import Path

from ruamel.yaml import YAML

from .exceptions import CredentialsNotFoundError

CREDENTIALS_PATH = Path(__file__).parent.with_name("strava-creds.yml")


# pylint: disable=too-few-public-methods
class Credentials:
    """Credentials used to log into the strava website."""

    username = ""
    password = ""

    @classmethod
    def gen_credentials(cls):
        """Generates credentials reading the credentials file (`strava-creds.yml`).

        Raises:
            CredentialsNotFoundError: if the credentials file doesn't exist.

        Returns:
            Credentials: strava credentials.
        """

        username = environ.get("STRAVA_USERNAME")
        password = environ.get("STRAVA_PASSWORD")

        if username and password:
            cls.username = username
            cls.password = password
            return cls()

        if not CREDENTIALS_PATH.is_file():
            with CREDENTIALS_PATH.open("wt", encoding="utf8") as file_handler:
                YAML().dump({"email": None, "password": None}, file_handler)

            logger = getLogger(__name__)
            logger.critical("Credentials not found")
            raise CredentialsNotFoundError("Credentials not found")

        data = YAML().load(CREDENTIALS_PATH.read_text())
        cls.username = data["email"]
        cls.password = data["password"]
        return cls()


credentials = Credentials.gen_credentials()
