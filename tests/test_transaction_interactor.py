"""
Test List:
1) Should transfer funds from one wallet to another.    👾
2) Should update balance of wallets in all currencies.  👾
"""
import pytest

from core import (
    InvalidApiKeyException,
    TransactionInteractor,
    UserInteractor,
    WalletInteractor,
)
from stubs.configuration import StubSystemConfiguration
from stubs.currency_converter import StubCurrencyConverter
from utils import random_api_key, random_string


def test_should_transfer_funds_for_user(
    user_interactor: UserInteractor,
    wallet_interactor: WalletInteractor,
    transaction_interactor: TransactionInteractor,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> None:
    currency_converter.exchange_rate = 2
    system_configuration.initial_balance = 1
    system_configuration.same_user_transfer_fee = 50  # Percent

    key = user_interactor.create_user(random_string())
    wallet_1 = wallet_interactor.create_wallet(api_key=key)
    wallet_2 = wallet_interactor.create_wallet(api_key=key)

    transaction_interactor.transfer(
        api_key=key,
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount_btc=0.5,
    )

    new_wallet_1 = wallet_interactor.get_wallet(address=wallet_1.address, api_key=key)
    new_wallet_2 = wallet_interactor.get_wallet(address=wallet_2.address, api_key=key)

    assert new_wallet_1.balance_btc == 0.5
    assert new_wallet_1.balance_usd == 1
    assert new_wallet_2.balance_btc == 1.25
    assert new_wallet_2.balance_usd == 2.5


def test_should_transfer_funds_between_users(
    user_interactor: UserInteractor,
    wallet_interactor: WalletInteractor,
    transaction_interactor: TransactionInteractor,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> None:
    currency_converter.exchange_rate = 5
    system_configuration.initial_balance = 2
    system_configuration.cross_user_transfer_fee = 25  # Percent

    key_1 = user_interactor.create_user("User 1")
    wallet_1 = wallet_interactor.create_wallet(api_key=key_1)

    key_2 = user_interactor.create_user("User 2")
    wallet_2 = wallet_interactor.create_wallet(api_key=key_2)

    transaction_interactor.transfer(
        api_key=key_1,
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount_btc=2,
    )

    new_wallet_1 = wallet_interactor.get_wallet(address=wallet_1.address, api_key=key_1)
    new_wallet_2 = wallet_interactor.get_wallet(address=wallet_2.address, api_key=key_2)

    assert new_wallet_1.balance_btc == 0
    assert new_wallet_1.balance_usd == 0
    assert new_wallet_2.balance_btc == 3.5
    assert new_wallet_2.balance_usd == 17.5


def test_should_not_transfer_funds_with_incorrect_api_key(
    user_interactor: UserInteractor,
    wallet_interactor: WalletInteractor,
    transaction_interactor: TransactionInteractor,
) -> None:
    correct_key = user_interactor.create_user(random_string())
    wallet_1 = wallet_interactor.create_wallet(api_key=correct_key)
    wallet_2 = wallet_interactor.create_wallet(api_key=correct_key)

    incorrect_key = random_api_key()

    with pytest.raises(InvalidApiKeyException):
        transaction_interactor.transfer(
            api_key=incorrect_key,
            source_address=wallet_1.address,
            destination_address=wallet_2.address,
            amount_btc=0.5,
        )


def test_should_return_correct_currencies_after_exchange_rate_change_before_transaction(
    user_interactor: UserInteractor,
    wallet_interactor: WalletInteractor,
    transaction_interactor: TransactionInteractor,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> None:
    currency_converter.exchange_rate = 5
    system_configuration.initial_balance = 2

    key_1 = user_interactor.create_user("User 1")
    wallet_1 = wallet_interactor.create_wallet(api_key=key_1)

    key_2 = user_interactor.create_user("User 2")
    wallet_2 = wallet_interactor.create_wallet(api_key=key_2)

    currency_converter.exchange_rate = 10

    transaction_interactor.transfer(
        api_key=key_1,
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount_btc=2,
    )

    new_wallet_1 = wallet_interactor.get_wallet(address=wallet_1.address, api_key=key_1)
    new_wallet_2 = wallet_interactor.get_wallet(address=wallet_2.address, api_key=key_2)

    assert new_wallet_1.balance_btc == 0
    assert new_wallet_1.balance_usd == 0
    assert new_wallet_2.balance_btc == 4
    assert new_wallet_2.balance_usd == 40


def test_should_return_correct_currencies_after_exchange_rate_change_after_transaction(
    user_interactor: UserInteractor,
    wallet_interactor: WalletInteractor,
    transaction_interactor: TransactionInteractor,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> None:
    currency_converter.exchange_rate = 5
    system_configuration.initial_balance = 2

    key_1 = user_interactor.create_user("User 1")
    wallet_1 = wallet_interactor.create_wallet(api_key=key_1)

    key_2 = user_interactor.create_user("User 2")
    wallet_2 = wallet_interactor.create_wallet(api_key=key_2)

    transaction_interactor.transfer(
        api_key=key_1,
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount_btc=2,
    )

    currency_converter.exchange_rate = 10

    new_wallet_1 = wallet_interactor.get_wallet(address=wallet_1.address, api_key=key_1)
    new_wallet_2 = wallet_interactor.get_wallet(address=wallet_2.address, api_key=key_2)

    assert new_wallet_1.balance_btc == 0
    assert new_wallet_1.balance_usd == 0
    assert new_wallet_2.balance_btc == 4
    assert new_wallet_2.balance_usd == 40
