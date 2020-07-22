"""Manages outgoing connections."""

from logging import getLogger

from bs4 import BeautifulSoup
from requests import ConnectionError as ReqConnectionError, Session as ReqSession

from .credentials import credentials
from .exceptions import LoginError


class Session(ReqSession):
    """HTTP session to get data from the strava website."""

    def __init__(self):
        super().__init__()
        self.headers.update({"user-agent": "strava-py"})

        self.logger = getLogger(__name__)
        self.retries = 5
        self.primary_url = "https://www.strava.com/dashboard"
        self.login_url = "https://www.strava.com/session"
        self.data_url = "https://www.strava.com/dashboard/following/1000"
        self.logged_in = False
        self.logging_in = False

    def login(self):
        """Logs into the strava website."""

        self.logger.debug("Logging in")
        self.logging_in = True
        response = self.get(self.primary_url)
        soup = BeautifulSoup(response.text, "html.parser")
        utf8 = soup.find("input", {"name": "utf8"})["value"]
        token = soup.find("input", {"name": "authenticity_token"})["value"]

        payload = {
            "email": credentials.username,
            "password": credentials.password,
            "utf8": utf8,
            "authenticity_token": token,
            "plan": "",
        }

        response = self.post(self.login_url, data=payload)
        if "/login" in response.url:
            raise LoginError("Credentials are not valid")

        self.headers.update({"x-csrf-token": token})
        self.logger.debug("Logged in")
        self.logged_in = True
        self.logging_in = False

    def request(self, *args, **kwargs):
        if not self.logged_in and not self.logging_in:
            self.login()

        retries = self.retries
        while retries:
            try:
                return super().request(*args, **kwargs)
            except ReqConnectionError as exc:
                retries -= 1
                if not retries:
                    raise ConnectionError from exc


session = Session()
