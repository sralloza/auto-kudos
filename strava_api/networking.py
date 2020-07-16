"""Manages outgoing connections."""

from logging import getLogger
from bs4 import BeautifulSoup
from requests import Session as ReqSession
from .credentials import credentials


class Session(ReqSession):
    """HTTP session to get data from the strava website."""

    def __init__(self):
        super().__init__()
        self.headers.update({"user-agent": "strava-py"})

        self.logger = getLogger(__name__)
        self.primary_url = "https://www.strava.com/dashboard"
        self.login_url = "https://www.strava.com/session"
        self.data_url = "https://www.strava.com/dashboard/following/1000"

        self.login()

    def login(self):
        """Logs into the strava website."""

        self.logger.debug("Logging in")
        print("Logging in")
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
        self.headers.update({"x-csrf-token": token})
        self.logger.debug("Logged in")


session = Session()
