from pathlib import Path
from unittest import mock

import pytest

from strava_api.credentials import CREDENTIALS_PATH, Credentials
from strava_api.exceptions import CredentialsNotFoundError


def test_credentials_path():
    relative = Path(__file__).relative_to(CREDENTIALS_PATH.parent)
    assert relative == Path("tests/test_credentials.py")
    assert CREDENTIALS_PATH.suffix == ".yml"


class TestGenCredentials:
    @pytest.fixture(autouse=True)
    def mocks(self):
        self.environ_m = mock.patch("strava_api.credentials.environ").start()
        self.creds_path_m = mock.patch(
            "strava_api.credentials.CREDENTIALS_PATH"
        ).start()
        self.yaml_m = mock.patch("strava_api.credentials.YAML").start()
        yield
        mock.patch.stopall()

    def test_no_creds_fail(self, caplog):
        self.environ_m.get = dict().get
        self.creds_path_m.is_file.return_value = False
        caplog.set_level(10, "strava_api.credentials")

        with pytest.raises(CredentialsNotFoundError, match="Credentials not found"):
            Credentials.gen_credentials()

        data = {"email": None, "password": None}
        self.creds_path_m.open.assert_called_once_with("wt", encoding="utf8")
        self.creds_path_m.open.return_value.__enter__.assert_called_once()
        self.creds_path_m.open.return_value.__exit__.assert_called_once()
        file_handler = self.creds_path_m.open.return_value.__enter__.return_value
        self.yaml_m.assert_called_once_with()
        self.yaml_m.return_value.dump.assert_called_with(data, file_handler)

        assert len(caplog.records) == 1
        assert caplog.records[0].message == "Credentials not found"
        assert caplog.records[0].levelname == "CRITICAL"

    @pytest.mark.parametrize("exc", [OSError, PermissionError])
    def test_no_creds_fail_permission_error(self, caplog, exc):
        self.creds_path_m.open.side_effect = exc
        self.environ_m.get = dict().get
        self.creds_path_m.is_file.return_value = False
        caplog.set_level(10, "strava_api.credentials")

        with pytest.raises(CredentialsNotFoundError, match="Credentials not found"):
            Credentials.gen_credentials()

        self.creds_path_m.open.assert_called_once_with("wt", encoding="utf8")
        self.creds_path_m.open.return_value.__enter__.assert_not_called()
        self.creds_path_m.open.return_value.__exit__.assert_not_called()
        self.yaml_m.assert_not_called()
        self.yaml_m.return_value.dump.assert_not_called()

        assert len(caplog.records) == 2
        assert caplog.records[0].message == "Couldn't create sample credentials"
        assert caplog.records[0].levelname == "ERROR"
        assert caplog.records[1].message == "Credentials not found"
        assert caplog.records[1].levelname == "CRITICAL"

    @pytest.mark.parametrize("mode", ["env", "file"])
    def test_ok(self, caplog, mode):
        if mode == "env":
            creds = {"STRAVA_USERNAME": "email@example.com", "STRAVA_PASSWORD": "pass"}
            self.environ_m.get = creds.get
            self.creds_path_m.is_file.return_value = False
        else:
            self.environ_m.get = dict().get
            self.creds_path_m.is_file.return_value = True
        caplog.set_level(10, "strava_api.credentials")

        data = {"email": "email@example.com", "password": "pass"}
        self.yaml_m.return_value.load.return_value = data

        credentials = Credentials.gen_credentials()
        assert isinstance(credentials, Credentials)

        if mode == "file":
            self.creds_path_m.read_text.assert_called_once_with()
            file_content = self.creds_path_m.read_text.return_value
            self.yaml_m.assert_called_once_with()
            self.yaml_m.return_value.load.assert_called_with(file_content)

        assert Credentials.username == "email@example.com"
        assert Credentials.password == "pass"

        assert len(caplog.records) == 0
