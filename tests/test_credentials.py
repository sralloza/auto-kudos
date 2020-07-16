from pathlib import Path
from unittest import mock

import pytest

from strava_api.credentials import CREDENTIALS_PATH, Credentials
from strava_api.exceptions import CredentialsNotFoundError


def test_credentials_path():
    relative = Path(__file__).relative_to(CREDENTIALS_PATH.parent)
    assert relative == Path("tests/test_credentials.py")
    assert CREDENTIALS_PATH.suffix == ".yml"


@mock.patch("strava_api.credentials.CREDENTIALS_PATH")
@mock.patch("strava_api.credentials.YAML")
def test_gen_credentials_fail(yaml_m, creds_path_m, caplog):
    creds_path_m.is_file.return_value = False
    caplog.set_level(10, "strava_api.credentials")

    with pytest.raises(CredentialsNotFoundError, match="Credentials not found"):
        Credentials.gen_credentials()

    data = {"email": None, "password": None}
    creds_path_m.open.assert_called_once_with("wt", encoding="utf8")
    creds_path_m.open.return_value.__enter__.assert_called_once()
    creds_path_m.open.return_value.__exit__.assert_called_once()
    file_handler = creds_path_m.open.return_value.__enter__.return_value
    yaml_m.assert_called_once_with()
    yaml_m.return_value.dump.assert_called_with(data, file_handler)

    assert len(caplog.records) == 1
    assert caplog.records[0].message == "Credentials not found"
    assert caplog.records[0].levelname == "CRITICAL"


@mock.patch("strava_api.credentials.CREDENTIALS_PATH")
@mock.patch("strava_api.credentials.YAML")
def test_gen_credentials_ok(yaml_m, creds_path_m, caplog):
    creds_path_m.is_file.return_value = True
    caplog.set_level(10, "strava_api.credentials")

    data = {"email": "email@example.com", "password": "pass"}
    yaml_m.return_value.load.return_value = data

    Credentials.gen_credentials()

    creds_path_m.read_text.assert_called_once_with()
    file_content = creds_path_m.read_text.return_value
    yaml_m.assert_called_once_with()
    yaml_m.return_value.load.assert_called_with(file_content)

    assert Credentials.username == "email@example.com"
    assert Credentials.password == "pass"

    assert len(caplog.records) == 0
