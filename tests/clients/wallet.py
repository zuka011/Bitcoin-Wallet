from dataclasses import dataclass

from infra import CreateWalletRequest, FetchWalletRequest
from requests import Response
from starlette.testclient import TestClient


@dataclass
class WalletClient:
    test_client: TestClient

    def create_wallet(self, *, api_key: str) -> Response:
        """Sends a POST request to create a wallet."""
        return self.test_client.post(
            "/wallets", data=CreateWalletRequest(api_key=api_key).json()
        )

    def fetch_wallet(self, *, wallet_address: str, api_key: str) -> Response:
        """Sends a GET request to fetch a wallet."""
        return self.test_client.get(
            f"/wallets/{wallet_address}",
            data=FetchWalletRequest(api_key=api_key).json(),
        )
