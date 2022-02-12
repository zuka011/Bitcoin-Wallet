from dataclasses import dataclass

from infra import FetchStatisticsRequest
from requests import Response
from starlette.testclient import TestClient


@dataclass
class StatisticsClient:
    test_client: TestClient

    def fetch_statistics(self, *, api_key: str) -> Response:
        """Submits a GET request to retrieve the platform statistics."""
        return self.test_client.get(
            "/statistics", data=FetchStatisticsRequest(api_key=api_key).json()
        )
