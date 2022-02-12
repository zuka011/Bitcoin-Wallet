"""
Test List:
1) Should transfer funds from one wallet to another.    👾
2) Should update balance of wallets in all currencies.  👾
"""

import pytest
from core import (
    Currency,
    InvalidApiKeyException,
    Transaction,
    TransactionInteractor,
    UserInteractor,
    WalletInteractor,
)
from stubs.configuration import StubSystemConfiguration
from stubs.currency_converter import StubCurrencyConverter
from utils import random_api_key, random_string

expected_source_address: str
expected_destination_address: str
expected_amount: float


def expect(
    *,
    source_address: str,
    destination_address: str,
    amount: float,
) -> None:
    """Prepares an expectation for a transaction."""
    global expected_source_address, expected_destination_address, expected_amount

    expected_source_address = source_address
    expected_destination_address = destination_address
    expected_amount = amount


def given(transaction: Transaction) -> None:
    """Checks the specified transaction against the built expectations."""
    assert transaction is not None

    assert transaction.source_address == expected_source_address
    assert transaction.destination_address == expected_destination_address
    assert transaction.amount == expected_amount


def test_should_transfer_funds_for_user(
    user_interactor: UserInteractor,
    wallet_interactor: WalletInteractor,
    transaction_interactor: TransactionInteractor,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> None:
    currency_converter.btc_to_usd = 2
    system_configuration.initial_balance = 1
    system_configuration.same_user_transfer_fee = 50  # Percent

    key = user_interactor.create_user(random_string())
    wallet_1 = wallet_interactor.create_wallet(api_key=key)
    wallet_2 = wallet_interactor.create_wallet(api_key=key)

    transaction_interactor.transfer(
        api_key=key,
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount=0.5,
    )

    new_wallet_1 = wallet_interactor.get_wallet(address=wallet_1.address, api_key=key)
    new_wallet_2 = wallet_interactor.get_wallet(address=wallet_2.address, api_key=key)

    assert new_wallet_1.get_balance(currency=Currency.BTC) == 0.5
    assert new_wallet_1.get_balance(currency=Currency.USD) == 1
    assert new_wallet_2.get_balance(currency=Currency.BTC) == 1.25
    assert new_wallet_2.get_balance(currency=Currency.USD) == 2.5


def test_should_transfer_funds_between_users(
    user_interactor: UserInteractor,
    wallet_interactor: WalletInteractor,
    transaction_interactor: TransactionInteractor,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> None:
    currency_converter.btc_to_usd = 5
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
        amount=2,
    )

    new_wallet_1 = wallet_interactor.get_wallet(address=wallet_1.address, api_key=key_1)
    new_wallet_2 = wallet_interactor.get_wallet(address=wallet_2.address, api_key=key_2)

    assert new_wallet_1.get_balance(currency=Currency.BTC) == 0
    assert new_wallet_1.get_balance(currency=Currency.USD) == 0
    assert new_wallet_2.get_balance(currency=Currency.BTC) == 3.5
    assert new_wallet_2.get_balance(currency=Currency.USD) == 17.5


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
            amount=0.5,
        )


def test_should_return_transactions_for_wallet(
    user_interactor: UserInteractor,
    wallet_interactor: WalletInteractor,
    transaction_interactor: TransactionInteractor,
) -> None:
    key = user_interactor.create_user(random_string())
    wallet_1 = wallet_interactor.create_wallet(api_key=key)
    wallet_2 = wallet_interactor.create_wallet(api_key=key)

    transaction_interactor.transfer(
        api_key=key,
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount=0.5,
    )

    transactions_1 = tuple(
        transaction_interactor.get_transactions(
            wallet_address=wallet_1.address, api_key=key
        )
    )

    transactions_2 = tuple(
        transaction_interactor.get_transactions(
            wallet_address=wallet_2.address, api_key=key
        )
    )

    assert len(transactions_1) == 1
    assert len(transactions_2) == 1

    expect(
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount=0.5,
    )

    given(transactions_1[0])
    given(transactions_2[0])


def test_should_return_correct_currencies_after_exchange_rate_change_before_transaction(
    user_interactor: UserInteractor,
    wallet_interactor: WalletInteractor,
    transaction_interactor: TransactionInteractor,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> None:
    currency_converter.btc_to_usd = 5
    system_configuration.initial_balance = 2

    key_1 = user_interactor.create_user("User 1")
    wallet_1 = wallet_interactor.create_wallet(api_key=key_1)

    key_2 = user_interactor.create_user("User 2")
    wallet_2 = wallet_interactor.create_wallet(api_key=key_2)

    currency_converter.btc_to_usd = 10

    transaction_interactor.transfer(
        api_key=key_1,
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount=2,
    )

    new_wallet_1 = wallet_interactor.get_wallet(address=wallet_1.address, api_key=key_1)
    new_wallet_2 = wallet_interactor.get_wallet(address=wallet_2.address, api_key=key_2)

    assert new_wallet_1.get_balance(currency=Currency.BTC) == 0
    assert new_wallet_1.get_balance(currency=Currency.USD) == 0
    assert new_wallet_2.get_balance(currency=Currency.BTC) == 4
    assert new_wallet_2.get_balance(currency=Currency.USD) == 40


def test_should_return_correct_currencies_after_exchange_rate_change_after_transaction(
    user_interactor: UserInteractor,
    wallet_interactor: WalletInteractor,
    transaction_interactor: TransactionInteractor,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> None:
    currency_converter.btc_to_usd = 5
    system_configuration.initial_balance = 2

    key_1 = user_interactor.create_user("User 1")
    wallet_1 = wallet_interactor.create_wallet(api_key=key_1)

    key_2 = user_interactor.create_user("User 2")
    wallet_2 = wallet_interactor.create_wallet(api_key=key_2)

    transaction_interactor.transfer(
        api_key=key_1,
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount=2,
    )

    currency_converter.btc_to_usd = 10

    new_wallet_1 = wallet_interactor.get_wallet(address=wallet_1.address, api_key=key_1)
    new_wallet_2 = wallet_interactor.get_wallet(address=wallet_2.address, api_key=key_2)

    assert new_wallet_1.get_balance(currency=Currency.BTC) == 0
    assert new_wallet_1.get_balance(currency=Currency.USD) == 0
    assert new_wallet_2.get_balance(currency=Currency.BTC) == 4
    assert new_wallet_2.get_balance(currency=Currency.USD) == 40
