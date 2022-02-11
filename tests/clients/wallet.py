from dataclasses import dataclass

from requests import Response
from starlette.testclient import TestClient


@dataclass
class WalletClient:
    test_client: TestClient

    def create_wallet(self, *, api_key: str) -> Response:
        """Sends a POST request to create a wallet."""
        return
