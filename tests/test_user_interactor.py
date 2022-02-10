"""
Test List:
1) Users should be able to register.                👾
2) API keys should be unique.                       👾
3) User should not be able to register with duplicate username. ?
4) Should create wallet for users.                  👾
5) Should not create wallet for invalid users.      👾
6) Duplicate usernames should throw an exception.   👾
"""

import pytest
from core import InvalidUsernameException, UserInteractor
from hypothesis import given
from hypothesis.strategies import text
from infra.repositories import InMemoryUserRepository
from stubs.currency_converter import StubCurrencyConverter
from utils import random_string


def test_should_create_user_interactor(interactor: UserInteractor) -> None:
    assert interactor is not None


@given(user_name=text())
def test_should_create_user(user_name: str) -> None:
    interactor = UserInteractor(
        user_repository=InMemoryUserRepository(),
        currency_converter=StubCurrencyConverter(),
    )
    assert interactor.create_user(user_name) is not None


def test_should_create_multiple_users(interactor: UserInteractor) -> None:
    key_1 = interactor.create_user(f"{random_string()} 1")
    key_2 = interactor.create_user(f"{random_string()} 2")

    assert key_1 != key_2


def test_should_store_usernames_persistently(
    interactor: UserInteractor, memory_user_repository: InMemoryUserRepository
) -> None:
    interactor.create_user("User 1")
    assert memory_user_repository.has_username("User 1")


def test_should_store_api_keys_persistently(
    interactor: UserInteractor, memory_user_repository: InMemoryUserRepository
) -> None:
    key = interactor.create_user("User 1")
    assert memory_user_repository.has_api_key(key)


def test_should_not_allow_duplicate_names(interactor: UserInteractor) -> None:
    interactor.create_user("User 1")
    with pytest.raises(InvalidUsernameException):
        interactor.create_user("User 1")


@given(user_name=text(max_size=7))
def test_should_not_allow_short_names(user_name: str) -> None:
    interactor = UserInteractor(
        min_length=8,
        user_repository=InMemoryUserRepository(),
        currency_converter=StubCurrencyConverter(),
    )
    with pytest.raises(InvalidUsernameException):
        interactor.create_user(user_name)


@given(user_name=text(min_size=21))
def test_should_not_allow_long_names(user_name: str) -> None:
    interactor = UserInteractor(
        max_length=20,
        user_repository=InMemoryUserRepository(),
        currency_converter=StubCurrencyConverter(),
    )
    with pytest.raises(InvalidUsernameException):
        interactor.create_user(user_name)
