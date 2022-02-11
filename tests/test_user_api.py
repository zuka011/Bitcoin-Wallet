from clients.user import UserClient
from infra import CreateUserResponse, InMemoryUserRepository
from response_utils import parse_response
from utils import random_string


def test_should_create_user(
    user_client: UserClient, memory_user_repository: InMemoryUserRepository
) -> None:
    username = random_string()
    response = user_client.create_user(username)
    api_key = parse_response(response, CreateUserResponse).api_key

    assert memory_user_repository.has_api_key(api_key)
    assert memory_user_repository.has_username(username)
