from dataclasses import dataclass

import pytest
from infra import CreateUserResponse, InMemoryUserRepository
from requests import Response
from response_utils import parse_response
from starlette.testclient import TestClient
from utils import random_string


@dataclass
class Client:
    test_client: TestClient

    def create_user(self, username: str) -> Response:
        """Sends a POST request to create a user."""
        return self.test_client.post(f"/users/{username}")


@pytest.fixture
def client(test_client: TestClient) -> Client:
    return Client(test_client)


def test_should_create_user(
    client: Client, memory_user_repository: InMemoryUserRepository
) -> None:
    username = random_string()
    response = client.create_user(username)
    api_key = parse_response(response, CreateUserResponse).api_key

    assert memory_user_repository.has_api_key(api_key)
    assert memory_user_repository.has_username(username)
