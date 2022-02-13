from dataclasses import dataclass

from requests import Response
from starlette.testclient import TestClient


@dataclass
class StatisticsClient:
    test_client: TestClient

    def fetch_statistics(self, *, api_key: str) -> Response:
        """Submits a GET request to retrieve the platform statistics."""
        return self.test_client.get("/statistics", headers={"api-key": api_key})
