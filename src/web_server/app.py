from pathlib import Path

from account_launcher.account_launcher import AccountLauncher
from flask import Flask

from .routes.routes import setup_routes
from .services.account_manager import AccountManager


class WebServer:
    def __init__(
        self,
        account_launcher: AccountLauncher,
        host: str = "127.0.0.1",
        port: int = 5000,
    ):
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.data_path = Path(__file__).parent.parent.resolve() / "data"

        self.account_launcher = account_launcher
        self.account_manager = AccountManager(self.data_path)

        setup_routes(self.app, self.account_manager, self.account_launcher)

    def run(self):
        self.app.run(host=self.host, port=self.port)
