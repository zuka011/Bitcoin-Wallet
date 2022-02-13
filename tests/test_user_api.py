from typing import List

from clients.user import UserClient
from core import DuplicateUsernameValidator, IUsernameValidator
from infra import CreateUserResponse, Error, InMemoryUserRepository
from response_utils import parse_response
from starlette import status
from utils import random_string


def test_should_create_user(
    user_client: UserClient, memory_user_repository: InMemoryUserRepository
) -> None:
    username = random_string()
    response = user_client.create_user(username)
    api_key = parse_response(response, CreateUserResponse).api_key

    assert memory_user_repository.has_api_key(api_key)
    assert memory_user_repository.has_username(username)

    assert response.status_code == status.HTTP_201_CREATED


def test_should_not_create_user_with_duplicate_username(
    user_client: UserClient,
    memory_user_repository: InMemoryUserRepository,
    username_validators: List[IUsernameValidator],
) -> None:
    username_validators.append(
        DuplicateUsernameValidator(user_repository=memory_user_repository)
    )

    username = random_string()
    user_client.create_user(username)

    response = user_client.create_user(username)
    error = parse_response(response, Error)

    assert error.error_message is not None
    assert response.status_code == status.HTTP_409_CONFLICT
