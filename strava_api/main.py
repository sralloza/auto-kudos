import logging
from pathlib import Path

from .data import give_kudos_to_everyone

fmt = "[%(asctime)s] %(levelname)s - %(name)s:%(lineno)s - %(message)s"
filename = Path(__file__).with_name("auto-kudos.log")
handlers = [logging.FileHandler(filename, "at", "utf-8")]
logging.basicConfig(level=10, format=fmt, handlers=handlers)
logging.getLogger("urllib3.connectionpool").setLevel(60)


def main():
    give_kudos_to_everyone()
