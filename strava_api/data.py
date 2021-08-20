"""Manages data parsing."""

from logging import getLogger
from typing import List

from bs4 import BeautifulSoup
from json import loads

from .activity import Activity
from .networking import Session


def get_activities() -> List[Activity]:
    """Gets all the activities from the strava website.

    Returns:
        List[Activity]: list of activities found.
    """

    logger = getLogger(__name__)
    session = Session()
    response = session.get(session.data_url)
    soup = BeautifulSoup(response.text, "html.parser")

    raw_activity_list = soup.find_all("div", {"data-react-class": "Activity"})

    parsed_activity_list = []
    for activity in raw_activity_list:
        activity_data = loads(activity["data-react-props"])["activity"]
        activity_id = int(activity_data["id"])
        can_give_kudo = bool(activity_data["kudosAndComments"]["canKudo"])
        title = activity_data["activityName"]
        user = activity_data["athlete"]["athleteName"]

        act = Activity(user, activity_id, title, not can_give_kudo)
        parsed_activity_list.append(act)

    logger.info("Found %s activities", len(parsed_activity_list))
    return parsed_activity_list


def give_kudos_to_everyone():
    """Gives a kudo to every activity found."""
    logger = getLogger(__name__)

    activities = get_activities()
    logger.info(
        "Found %d potential kudo givings", sum((not x.has_kudo for x in activities))
    )
    for activity in activities:
        activity.ensure_kudo()
