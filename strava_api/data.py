"""Manages data parsing."""

from logging import getLogger
from typing import List

from bs4 import BeautifulSoup

from .activity import Activity
from .networking import session


def get_activities() -> List[Activity]:
    """Gets all the activities from the strava website.

    Returns:
        List[Activity]: list of activities found.
    """

    logger = getLogger(__name__)
    response = session.get(session.data_url)
    soup = BeautifulSoup(response.text, "html.parser")

    activities = soup.find_all("div", class_="activity feed-entry card")

    acts = []
    for activity in activities:
        activity_id = int(activity["id"].split("-")[-1])
        kudo_button = activity.find("button", {"str-type": "kudos"})
        can_give_kudo = "give" in kudo_button["title"].lower()
        title = activity.find("h3", class_="title-text").text.strip()
        user = activity.find("a", class_="entry-owner").text.strip()

        act = Activity(user, activity_id, title, not can_give_kudo)
        acts.append(act)

    logger.info("Found %s activities", len(acts))
    return acts


def give_kudos_to_everyone():
    """Gives a kudo to every activity found."""

    activities = get_activities()
    for activity in activities:
        activity.give_kudo()
