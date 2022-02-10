"""
Test List:
1) Create a wallet
2) Wallet should contain a unique address and balance in BTC and USD
"""

import pytest
from core import InvalidApiKeyException, InvalidWalletRequestException, UserInteractor
from hypothesis import given
from hypothesis.strategies import text
from infra import InMemoryUserRepository
from infra.converters.currency_converter import CoinLayerCurrencyConverter
from stubs.currency_converter import StubCurrencyConverter
from utils import random_string


@given(user_name=text())
def test_should_create_wallet_for_user(user_name: str) -> None:
    interactor = UserInteractor(
        user_repository=InMemoryUserRepository(),
        currency_converter=StubCurrencyConverter(),
    )

    key = interactor.create_user(user_name)

    assert interactor.create_wallet(key) is not None


def test_should_not_create_wallet_for_invalid_user(interactor: UserInteractor) -> None:
    key = random_string()

    with pytest.raises(InvalidApiKeyException):
        interactor.create_wallet(key)


def test_should_not_create_too_many_wallets() -> None:
    interactor = UserInteractor(
        user_repository=InMemoryUserRepository(),
        currency_converter=StubCurrencyConverter(),
        wallet_limit=3,
    )

    key = interactor.create_user("Bla bla user")
    interactor.create_wallet(key)
    interactor.create_wallet(key)
    interactor.create_wallet(key)

    with pytest.raises(InvalidWalletRequestException):
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


def test_should_get_real_time_balance() -> None:
    assert CoinLayerCurrencyConverter.to_usd(5) is not None
