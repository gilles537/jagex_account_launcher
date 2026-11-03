import json
import sys
from pathlib import Path

from account_launcher.account_launcher import AccountLauncher
from loguru import logger
from web_server.app import WebServer

_BASE_PATH = Path(__file__).parent.resolve()
SETTINGS_PATH = _BASE_PATH / "data" / "settings.json"

def main() -> None:
    with open(SETTINGS_PATH) as f:
        settings = json.load(f)

    logger.remove()
    logger.add(sys.stderr, level=settings["log_level"].upper())

    logger.info("Initializing web server")
    account_launcher = AccountLauncher(settings=settings)
    web_server = WebServer(account_launcher=account_launcher)

    try:
        web_server.run()
    except KeyboardInterrupt:
        logger.info("Got keyboard interrupt, exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()
