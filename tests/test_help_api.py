from dataclasses import dataclass

import pytest
from infra import FetchHelpResponse
from requests import Response
from response_utils import parse_response
from starlette import status
from starlette.testclient import TestClient


@dataclass
class Client:
    test_client: TestClient

    def fetch_help(self) -> Response:
        """Sends a GET request to the test client to fetch the help message."""
        return self.test_client.get("/")


@pytest.fixture
def client(test_client: TestClient) -> Client:
    return Client(test_client)


def test_should_fetch_help_message(client: Client) -> None:
    response = client.fetch_help()
    content = parse_response(response, FetchHelpResponse)

    assert response.status_code == status.HTTP_200_OK
    assert content.help_message != ""
