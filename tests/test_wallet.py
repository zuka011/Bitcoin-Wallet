"""
Test List:
1) Create a wallet
2) Wallet should contain a unique address and balance in BTC and USD
"""

import pytest
from core import InvalidApiKeyException, UserInteractor
from core.users.interactor import StubCurrencyConverter
from hypothesis import given
from hypothesis.strategies import text
from infra import InMemoryUserRepository
from utils import random_string


@given(user_name=text())
def test_should_create_wallet_for_user(user_name: str) -> None:
    interactor = UserInteractor(user_repository=InMemoryUserRepository())

    key = interactor.create_user(user_name)

    assert interactor.create_wallet(key) is not None


def test_should_not_create_wallet_for_invalid_user(interactor: UserInteractor) -> None:
    key = random_string()

    with pytest.raises(InvalidApiKeyException):
        interactor.create_wallet(key)


def test_should_create_unique_address_for_user(interactor: UserInteractor) -> None:
    key = interactor.create_user(random_string())
    assert (
        interactor.create_wallet(key).address != interactor.create_wallet(key).address
    )


def test_should_return_correct_balance() -> None:
    interactor = UserInteractor(
        user_repository=InMemoryUserRepository(),
        initial_balance=1,
        currency_converter=StubCurrencyConverter(2),
    )
    key = interactor.create_user(random_string())
    wallet = interactor.create_wallet(key)
    assert wallet.balance_btc == 1
    assert wallet.balance_usd == 2
