from pathlib import Path
from unittest import mock

from strava_api.activity import Activity
from strava_api.data import get_activities, give_kudos_to_everyone


@mock.patch("strava_api.data.Session")
def test_get_activities(session_m):
    data_path = Path(__file__).parent.joinpath("test_data/example.html.data")
    session_m.return_value.get.return_value.text = data_path.read_text(encoding="utf8")
    activities = get_activities()
    for i, act in enumerate(activities):
        i += 1
        assert act == Activity(f"Owner-{i}", i, f"Activity-{i}", i != 19)
    session_m.assert_called_once_with()
    session_m.return_value.get.assert_called_once()


@mock.patch("strava_api.data.get_activities")
def test_give_kudos_to_everyone(get_acts_m):
    mymock = mock.MagicMock()
    get_acts_m.return_value = [mymock] * 15

    give_kudos_to_everyone()
    mymock.ensure_kudo.assert_called_with()
    assert mymock.ensure_kudo.call_count == 15
