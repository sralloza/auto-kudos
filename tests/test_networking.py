from logging import Logger
from pathlib import Path
from unittest import mock

import pytest
from requests import ConnectionError as ReqConnectionError

from strava_api.exceptions import LoginError
from strava_api.networking import Session


class TestSession:
    @pytest.fixture(autouse=True)
    def mocks(self):
        Session._instances = {}  # pylint: disable=protected-access
        self.real_req_m = mock.patch("strava_api.networking.ReqSession.request").start()
        self.req_m_handler = mock.patch("strava_api.networking.Session.request")
        self.req_m = self.req_m_handler.start()
        self.get_m_handler = mock.patch("strava_api.networking.Session.get")
        self.get_m = self.get_m_handler.start()
        self.post_m = mock.patch("strava_api.networking.Session.post").start()
        self.creds_m = mock.patch("strava_api.networking.credentials").start()

        yield
        mock.patch.stopall()

    def test_singleton(self):
        session_1 = Session()
        session_2 = Session()
        assert session_1 is session_2

    def test_attributes(self):
        session = Session()
        assert hasattr(session, "logger")
        assert isinstance(session.logger, Logger)

        assert hasattr(session, "retries")
        assert isinstance(session.retries, int)

        assert hasattr(session, "primary_url")
        assert isinstance(session.primary_url, str)
        assert "strava" in session.primary_url
        assert "https://" in session.primary_url
        assert "dashboard" in session.primary_url

        assert hasattr(session, "login_url")
        assert isinstance(session.login_url, str)
        assert "strava" in session.login_url
        assert "https://" in session.login_url
        assert "session" in session.login_url

        assert hasattr(session, "data_url")
        assert isinstance(session.data_url, str)
        assert "strava" in session.data_url
        assert "https://" in session.data_url
        assert "dashboard" in session.data_url

        assert hasattr(session, "logged_in")
        assert isinstance(session.logged_in, bool)

        assert hasattr(session, "logging_in")
        assert isinstance(session.logging_in, bool)

        self.req_m.assert_not_called()

    @pytest.mark.parametrize("fail", [False, True])
    def test_login(self, fail):
        self.creds_m.username = "<username>"
        self.creds_m.password = "<password>"
        login_page_path = Path(__file__).parent.joinpath(
            "test_data/login_page.html.data"
        )
        login_page = login_page_path.read_text(encoding="utf8")

        get_response = mock.MagicMock()
        get_response.text.read.return_value = login_page
        self.get_m.return_value = get_response

        post_response = mock.MagicMock()
        if not fail:
            post_response.url = "https://www.strava.com/dashboard"
        else:
            post_response.url = "https://www.strava.com/login"
        self.post_m.return_value = post_response

        if fail:
            with pytest.raises(LoginError, match="Credentials are not valid"):
                Session().login()
        else:
            Session().login()

        assert self.req_m.call_count == 0

        data = {
            "email": "<username>",
            "password": "<password>",
            "utf8": "✓",
            "authenticity_token": "9Q2bgQuWYnUSlgQYz0XFGMRUyhlBeSdHOckVNPzB9Mpeeu"
            + "cwIVqAbyVCfK0u33pqNXuLG9GnhjShhFTZJ2lefw==",
            "plan": "",
        }

        self.get_m.assert_called_once_with(mock.ANY)
        self.post_m.assert_called_once_with(mock.ANY, data=data)

    @pytest.mark.parametrize("retries", range(6))
    @pytest.mark.parametrize("fails", range(11))
    def test_retry_error(self, fails, retries):
        response = mock.MagicMock()
        self.real_req_m.side_effect = [ReqConnectionError] * fails + [response]
        self.get_m_handler.stop()
        self.req_m_handler.stop()
        session = Session()
        session.retries = retries
        session.logged_in = True
        will_fail = fails >= session.retries

        if will_fail:
            with pytest.raises(ConnectionError):
                session.get("some_url")
        else:
            real_response = session.get("some_url")
            assert real_response is response

    @mock.patch("strava_api.networking.Session.login")
    def test_auto_login(self, login_m):
        def new_login():
            ses.logged_in = True

        login_m.side_effect = new_login
        self.get_m_handler.stop()
        self.req_m_handler.stop()
        ses = Session()

        assert not ses.logged_in
        login_m.assert_not_called()

        ses.get("url")
        login_m.assert_called_once_with()
        assert ses.logged_in
