from dataclasses import dataclass

from requests import Response
from starlette.testclient import TestClient


@dataclass
class UserClient:
    test_client: TestClient

    def create_user(self, username: str) -> Response:
        """Sends a POST request to create a user."""
        return self.test_client.post(f"/users/{username}")
