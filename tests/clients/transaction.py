from dataclasses import dataclass

from infra import CreateTransactionRequest
from requests import Response
from starlette.testclient import TestClient


@dataclass
class TransactionClient:
    test_client: TestClient

    def create_transaction(
        self,
        *,
        api_key: str,
        source_address: str,
        destination_address: str,
        amount: float,
    ) -> Response:
        """Submits a POST request to create a transaction."""
        return self.test_client.post(
            "/transactions",
            headers={"api-key": api_key},
            data=CreateTransactionRequest(
                source_address=source_address,
                destination_address=destination_address,
                amount=amount,
            ).json(),
        )

    def fetch_transactions(self, *, wallet_address: str, api_key: str) -> Response:
        """Submits a GET request to retrieve all wallet transactions."""
        return self.test_client.get(
            f"/wallets/{wallet_address}/transactions",
            headers={"api-key": api_key},
        )

    def fetch_user_transactions(self, *, api_key: str) -> Response:
        """Submits a GET request to retrieve all user transactions."""
        return self.test_client.get("/transactions", headers={"api-key": api_key})
