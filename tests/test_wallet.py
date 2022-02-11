"""
Test List:
1) Create a wallet
2) Wallet should contain a unique address and balance in BTC and USD
"""

import pytest
from core import InvalidApiKeyException, UserInteractor, WalletInteractor
from infra import InMemoryUserRepository
from infra.converters.currency_converter import CoinLayerCurrencyConverter
from stubs.currency_converter import StubCurrencyConverter
from utils import random_string


def test_should_create_wallet_for_user(
    user_interactor: UserInteractor,
    wallet_interactor: WalletInteractor,
    repository: InMemoryUserRepository,
) -> None:
    key = user_interactor.create_user(random_string())

    assert wallet_interactor.create_wallet(key) is not None


def test_should_not_create_wallet_for_invalid_user(
    wallet_interactor: WalletInteractor,
) -> None:
    key = random_string()

    with pytest.raises(InvalidApiKeyException):
        wallet_interactor.create_wallet(key)


def test_should_create_unique_wallet_address_for_user(
    user_interactor: UserInteractor, wallet_interactor: WalletInteractor
) -> None:
    key = user_interactor.create_user(random_string())
    assert (
        wallet_interactor.create_wallet(key).address
        != wallet_interactor.create_wallet(key).address
    )


def test_should_create_unique_wallet_address_across_users(
    user_interactor: UserInteractor, wallet_interactor: WalletInteractor
) -> None:
    key_1 = user_interactor.create_user(random_string())
    key_2 = user_interactor.create_user(random_string())
    assert (
        wallet_interactor.create_wallet(key_1).address
        != wallet_interactor.create_wallet(key_2).address
    )


def test_should_return_correct_balance(
    user_interactor: UserInteractor, repository: InMemoryUserRepository
) -> None:
    wallet_interactor = WalletInteractor(
        user_repository=repository,
        currency_converter=StubCurrencyConverter(exchange_rate=2),
        initial_balance=1,
    )

    key = user_interactor.create_user(random_string())
    wallet = wallet_interactor.create_wallet(key)
    assert wallet.balance_btc == 1
    assert wallet.balance_usd == 2


def test_should_retrieve_wallet(
    user_interactor: UserInteractor, wallet_interactor: WalletInteractor
) -> None:
    key = user_interactor.create_user(random_string())
    wallet = wallet_interactor.create_wallet(api_key=key)

    assert wallet_interactor.get_wallet(address=wallet.address) == wallet


def test_should_get_real_time_balance() -> None:
    assert CoinLayerCurrencyConverter.to_usd(5) is not None
