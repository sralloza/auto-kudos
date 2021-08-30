from pathlib import Path
from unittest import mock

from strava_api.activity import Activity
from strava_api.data import get_activities, give_kudos_to_everyone


@mock.patch("strava_api.data.Session")
def test_get_activities(session_m):
    data_path = Path(__file__).parent.joinpath("test_data/example.html.data")
    session_m.return_value.get.return_value.text = data_path.read_text(encoding="utf8")
    activities = get_activities()
    expected_activities = [
        Activity("Pepe", 5827388466, "Bicicleta por la mañana", True),
        Activity("Federico", 5801510087, "Actividad de tarde", True),
        Activity("Pedro", 5795292810, "Morcuera & Canencia ", True),
        Activity("Pepe", 5795160537, "Bicicleta por la mañana", True),
        Activity("Pepe", 5784888743, "Subida a la ermita", True),
        Activity("Pepe", 5779958345, "Bicicleta por la mañana", True),
        Activity("Pedro", 5758572558, "Morcuera & Canencia", True),
        Activity("Federico", 5751655113, "Ciclismo por la mañana", True),
        Activity("Pepe", 5746858402, "Bicicleta por la mañana", True),
        Activity("Luis", 5710064779, "Bicicleta por la mañana", True),
        Activity("Pedro", 5683333940, "Morning Ride", True),
        Activity("Alex", 5684536106, "Caminata a la hora del almuerzo", True),
        Activity("Alex", 5670246132, "Brujas", True),
        Activity("Luis", 5662393999, "Cabo Quintres", True),
        Activity("Luis", 5651487098, "Paseo ria", True),
        Activity("Rodrigo", 2391870897, "Evening Run", True),
        Activity("Pepe", 5641021478, "Bicicleta por la mañana", True),
        Activity("Alex", 5608849197, "Caminata de mañana", True),
        Activity("Pepe", 5603274730, "Bicicleta por la mañana", True),
    ]

    assert activities == expected_activities

    session_m.assert_called_once_with()
    session_m.return_value.get.assert_called_once()


@mock.patch("strava_api.data.get_activities")
def test_give_kudos_to_everyone(get_acts_m, caplog):
    caplog.set_level(10, "strava_api.data")

    mock_a = mock.MagicMock()
    mock_b = mock.MagicMock()

    mock_a.has_kudo = True
    mock_b.has_kudo = False

    get_acts_m.return_value = ([mock_a] * 5) + ([mock_b] * 10)

    give_kudos_to_everyone()
    mock_a.ensure_kudo.assert_called_with()
    assert mock_a.ensure_kudo.call_count == 5
    mock_b.ensure_kudo.assert_called_with()
    assert mock_b.ensure_kudo.call_count == 10

    assert len(caplog.records) == 1
    assert caplog.records[0].msg == "Found %d potential kudo givings"
    assert caplog.records[0].args == (10,)
