from unittest import mock

import pytest

from strava_api.activity import Activity


@pytest.fixture
def activity():
    yield Activity("username", 654, "title", False)


def test_attributes(activity):
    assert hasattr(activity, "username")
    assert hasattr(activity, "activity_id")
    assert hasattr(activity, "title")
    assert hasattr(activity, "has_kudo")


def test_kudo_endpoint(activity):
    assert "www.strava.com" in activity.kudo_endpoint
    assert isinstance(activity.kudo_endpoint, str)


@mock.patch("strava_api.activity.session.post")
def test_give_kudo(post_m, activity, caplog):
    caplog.set_level(10, "strava_api.activity")
    post_m.return_value.json.return_value = {"success": "true"}
    activity.give_kudo()

    post_m.assert_called_once_with(activity.kudo_endpoint)
    post_m.return_value.json.assert_called_once_with()

    assert len(caplog.records) == 2
    assert caplog.records[0].msg == "Giving kudo to %s"
    assert caplog.records[0].args == (activity, )
    assert caplog.records[1].message == "Result: true"
