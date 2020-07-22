"""Manages activity matters."""

from dataclasses import dataclass
from logging import getLogger

from .networking import Session


@dataclass
class Activity:
    """Represents an activity from Strava."""

    username: str
    activity_id: int
    title: str
    has_kudo: bool

    @property
    def kudo_endpoint(self) -> str:
        """Endpoint to make a post request when giving a kudo.

        Returns:
            str: endpoint.
        """
        return f"https://www.strava.com/feed/activity/{self.activity_id}/kudo"

    def give_kudo(self):
        """Gives a kudo to the user that did the activity."""

        logger = getLogger(__name__)
        session = Session()

        logger.debug("Giving kudo to %s", self)
        response = session.post(self.kudo_endpoint)
        result = response.json().get("success", False)
        logger.debug("Result: %s", result)

    def ensure_kudo(self):
        """If the activity has not a kudo, give it."""

        if not self.has_kudo:
            self.give_kudo()
