"""Install script designed only for testing."""

from pathlib import Path

from setuptools import setup

reqs = Path(__file__).with_name("requirements.txt").read_text().splitlines()
setup(name="auto-kudos", version="1.0", install_requires=reqs, packages=["strava_api"])
