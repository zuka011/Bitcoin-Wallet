"""
Test List:
1) Users should be able to register.            👾
2) API keys should be unique.                   👾
3) User should not be able to register with duplicate username. ?
4) Should create wallet for users.              👾
5) Should not create wallet for invalid users.  👾
"""

import string
from random import choice

import pytest
from core import InMemoryUserRepository, InvalidApiKeyException, UserInteractor
from hypothesis import example, given
from hypothesis.strategies import text


def random_string(length: int = 10) -> str:
    """Creates a random string."""
    return "".join([choice(string.ascii_letters) for _ in range(length)])


@pytest.fixture(scope="module")
def interactor() -> UserInteractor:
    return UserInteractor()


def test_should_create_user_interactor(interactor: UserInteractor) -> None:
    assert interactor is not None


@given(user_name=text())
@example(user_name="Jemali")
def test_should_create_user(interactor: UserInteractor, user_name: str) -> None:
    assert interactor.create_user(user_name) is not None


def test_should_create_multiple_users(interactor: UserInteractor) -> None:
    key_1 = interactor.create_user(f"{random_string()} 1")
    key_2 = interactor.create_user(f"{random_string()} 2")

    assert key_1 != key_2


@given(user_name=text())
def test_should_create_wallet_for_user(
        interactor: UserInteractor, user_name: str
) -> None:
    memory_repository = InMemoryUserRepository()
    interactor = UserInteractor(memory_repository)

    key = interactor.create_user(user_name)

    assert interactor.create_wallet(key) is not None


def test_should_not_create_wallet_for_invalid_user(interactor: UserInteractor) -> None:
    key = random_string()

    with pytest.raises(InvalidApiKeyException):
        interactor.create_wallet(key)


def test_should_store_api_keys_persistently() -> None:
    memory_repository = InMemoryUserRepository()

    interactor = UserInteractor(memory_repository)
    key = interactor.create_user("User 1")

    interactor = UserInteractor(memory_repository)
    assert interactor.create_wallet(key) is not None
