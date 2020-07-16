from pathlib import Path
from unittest import mock

import pytest

from strava_api.activity import Activity
from strava_api.data import get_activities


@mock.patch("strava_api.data.session.get")
def test_get_activities(get_m):
    get_m.return_value.text = (
        Path(__file__).with_name("example.html").read_text(encoding="utf8")
    )
    activities = get_activities()
    for i, act in enumerate(activities):
        i += 1
        assert act == Activity(f"Owner-{i}", i, f"Activity-{i}", i != 19)
