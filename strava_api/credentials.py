"""Manages credentials of the api."""

from logging import getLogger
from pathlib import Path

from ruamel.yaml import YAML

from .exceptions import CredentialsNotFoundError

CREDENTIALS_PATH = Path(__file__).parent.with_name("strava-creds.yml")


class Credentials:
    """Credentials used to log into the strava website."""

    username = ""
    password = ""

    if not CREDENTIALS_PATH.is_file():
        with CREDENTIALS_PATH.open("wt", encoding="utf8") as file_handler:
            YAML().dump({"email": None, "password": None}, file_handler)

        logger = getLogger(__name__)
        logger.critical("Credentials not found")
        raise CredentialsNotFoundError("Credentials not found")

    data = YAML().load(CREDENTIALS_PATH.read_text())
    username = data["email"]
    password = data["password"]
    del data


credentials = Credentials()
