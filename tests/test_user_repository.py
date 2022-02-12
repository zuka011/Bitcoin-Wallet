from typing import Any, Final

from conftest import memory_user_repository, sqlite_user_repository
from core import IUserRepository
from pytest_cases import parametrize
from utils import random_api_key, random_string

USER_REPOSITORIES: Final[Any] = [memory_user_repository, sqlite_user_repository]


@parametrize("user_repository", USER_REPOSITORIES)  # type: ignore
def test_should_add_users_to_repository(user_repository: IUserRepository) -> None:
    user_repository.add_user(api_key=random_api_key(), username=random_string())
    user_repository.add_user(api_key=random_api_key(), username=random_string())
    user_repository.add_user(api_key=random_api_key(), username=random_string())


@parametrize("user_repository", USER_REPOSITORIES)  # type: ignore
def test_should_get_api_keys_from_repository(user_repository: IUserRepository) -> None:
    key_1 = random_api_key()
    key_2 = random_api_key()
    key_3 = random_api_key()
    key_4 = random_api_key()

    user_repository.add_user(api_key=key_1, username=random_string())
    user_repository.add_user(api_key=key_2, username=random_string())
    user_repository.add_user(api_key=key_3, username=random_string())

    assert user_repository.has_api_key(key_1) is True
    assert user_repository.has_api_key(key_2) is True
    assert user_repository.has_api_key(key_3) is True
    assert user_repository.has_api_key(key_4) is False


@parametrize("user_repository", USER_REPOSITORIES)  # type: ignore
def test_should_get_usernames_from_repository(user_repository: IUserRepository) -> None:
    username_1 = random_string()
    username_2 = random_string()
    username_3 = random_string()
    username_4 = random_string()

    user_repository.add_user(api_key=random_api_key(), username=username_1)
    user_repository.add_user(api_key=random_api_key(), username=username_2)
    user_repository.add_user(api_key=random_api_key(), username=username_3)

    assert user_repository.has_username(username_1) is True
    assert user_repository.has_username(username_2) is True
    assert user_repository.has_username(username_3) is True
    assert user_repository.has_username(username_4) is False
