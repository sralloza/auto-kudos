"""Manages activity matters."""

from logging import getLogger

from .networking import Session


class Activity:
    """Represents an activity from Strava."""

    def __init__(self, username: str, activity_id: int, title: str, has_kudo: bool):
        self.username = str(username)
        self.id = int(activity_id)
        self.title = str(title)
        self.has_kudo = bool(has_kudo)

    def __repr__(self):
        template = "Activity(username={0.username!r}, id={0.id}, title={0.title!r}, has_kudo={0.has_kudo})"
        return template.format(self)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @property
    def kudo_endpoint(self) -> str:
        """Endpoint to make a post request when giving a kudo.

        Returns:
            str: endpoint.
        """
        return f"https://www.strava.com/feed/activity/{self.id}/kudo"

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
