import logging
import os
from json import loads

from strava_api.data import give_kudos_to_everyone


def aws_lambda(event: str, lambda_context):
    logger = logging.getLogger(__name__)
    try:
        if isinstance(event, str):
            data = loads(event)
        elif isinstance(event, dict):
            data = event
        else:
            raise TypeError(f"Invalid event type: {type(event).__name__!r}")
        if "username" in data:
            os.environ["STRAVA_USERNAME"] = data["username"]
        if "password" in data:
            os.environ["STRAVA_PASSWORD"] = data["password"]
    except Exception:
        logger.exception("Error loading event")

    give_kudos_to_everyone()
