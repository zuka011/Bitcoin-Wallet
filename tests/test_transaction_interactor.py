from dataclasses import dataclass
from typing import Iterable, List, Optional

import pytest
from core import (
    Currency,
    InvalidApiKeyException,
    Transaction,
    TransactionInteractor,
    UserInteractor,
    WalletInteractor,
)
from infra import InMemoryTransactionRepository
from stubs.configuration import StubSystemConfiguration
from stubs.currency_converter import StubCurrencyConverter
from utils import random_api_key, random_string


def sort_transactions(transactions: Iterable[Transaction]) -> List[Transaction]:
    """Returns a sorted list of all transactions in the specified iterable. The transactions
    are sorted by their timestamp in ascending order."""
    return sorted(transactions, key=lambda transaction: transaction.timestamp)


@dataclass(frozen=True)
class TransactionExpectation:
    expected_id: Optional[str]
    expected_source_address: str
    expected_destination_address: str
    expected_amount: float

    def given(self, transaction: Transaction) -> "TransactionExpectation":
        """Checks the specified transaction against the built expectations."""
        assert transaction is not None

        if self.expected_id is not None:
            assert transaction.id == self.expected_id

        assert transaction.source_address == self.expected_source_address
        assert transaction.destination_address == self.expected_destination_address
        assert transaction.amount == pytest.approx(self.expected_amount)

        return self


def expect_transaction(
    *,
    transaction_id: Optional[str] = None,
    source_address: str,
    destination_address: str,
    amount: float,
) -> TransactionExpectation:
    """Prepares an expectation for a transaction."""
    return TransactionExpectation(
        expected_id=transaction_id,
        expected_source_address=source_address,
        expected_destination_address=destination_address,
        expected_amount=amount,
    )


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

    transactions_1 = list(
        transaction_interactor.get_transactions(
            wallet_address=wallet_1.address, api_key=key
        )
    )

    transactions_2 = list(
        transaction_interactor.get_transactions(
            wallet_address=wallet_2.address, api_key=key
        )
    )

    assert len(transactions_1) == 1
    assert len(transactions_2) == 1

    expect_transaction(
        transaction_id=transactions_1[0].id,
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount=0.5,
    ).given(transactions_1[0]).given(transactions_2[0])


def test_should_return_transactions_between_users(
    user_interactor: UserInteractor,
    wallet_interactor: WalletInteractor,
    transaction_interactor: TransactionInteractor,
) -> None:
    key_1 = user_interactor.create_user(random_string())
    key_2 = user_interactor.create_user(random_string())
    wallet_1 = wallet_interactor.create_wallet(api_key=key_1)
    wallet_2 = wallet_interactor.create_wallet(api_key=key_2)

    transaction_interactor.transfer(
        api_key=key_1,
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount=0.5,
    )

    transaction_interactor.transfer(
        api_key=key_2,
        source_address=wallet_2.address,
        destination_address=wallet_1.address,
        amount=0.5,
    )

    transactions_1 = sort_transactions(
        transaction_interactor.get_transactions(
            wallet_address=wallet_1.address, api_key=key_1
        )
    )

    transactions_2 = sort_transactions(
        transaction_interactor.get_transactions(
            wallet_address=wallet_2.address, api_key=key_2
        )
    )

    assert len(transactions_1) == 2
    assert len(transactions_2) == 2

    expect_transaction(
        transaction_id=transactions_1[0].id,
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount=0.5,
    ).given(transactions_1[0]).given(transactions_2[0])

    expect_transaction(
        transaction_id=transactions_1[1].id,
        source_address=wallet_2.address,
        destination_address=wallet_1.address,
        amount=0.5,
    ).given(transactions_1[1]).given(transactions_2[1])


def test_should_include_transaction_fees_in_transactions(
    user_interactor: UserInteractor,
    wallet_interactor: WalletInteractor,
    transaction_interactor: TransactionInteractor,
    system_configuration: StubSystemConfiguration,
) -> None:
    key_1 = user_interactor.create_user(random_string())
    key_2 = user_interactor.create_user(random_string())
    wallet_1 = wallet_interactor.create_wallet(api_key=key_1)
    wallet_2 = wallet_interactor.create_wallet(api_key=key_2)

    system_configuration.cross_user_transfer_fee = 50  # Percent.

    transaction_interactor.transfer(
        api_key=key_1,
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount=0.5,
    )

    transactions_1 = sort_transactions(
        transaction_interactor.get_transactions(
            wallet_address=wallet_1.address, api_key=key_1
        )
    )

    transactions_2 = sort_transactions(
        transaction_interactor.get_transactions(
            wallet_address=wallet_2.address, api_key=key_2
        )
    )

    assert len(transactions_1) == 2
    assert len(transactions_2) == 1

    expect_transaction(
        transaction_id=transactions_1[0].id,
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount=0.25,
    ).given(transactions_1[0]).given(transactions_2[0])

    expect_transaction(
        source_address=wallet_1.address,
        destination_address=system_configuration.system_wallet_address,
        amount=0.25,
    ).given(transactions_1[1])


def test_should_store_transactions_persistently(
    user_interactor: UserInteractor,
    wallet_interactor: WalletInteractor,
    transaction_interactor: TransactionInteractor,
    memory_transaction_repository: InMemoryTransactionRepository,
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

    transactions_1 = list(
        memory_transaction_repository.get_transactions(wallet_address=wallet_1.address)
    )
    transactions_2 = list(
        memory_transaction_repository.get_transactions(wallet_address=wallet_2.address)
    )

    assert len(transactions_1) == 1
    assert len(transactions_2) == 1

    expect_transaction(
        transaction_id=transactions_1[0].id,
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount=0.5,
    ).given(
        Transaction(
            transaction_entry=transactions_1[0],
        )
    ).given(
        Transaction(
            transaction_entry=transactions_2[0],
        )
    )


def test_should_not_return_transactions_for_wallet_with_invalid_api_key(
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

    with pytest.raises(InvalidApiKeyException):
        transaction_interactor.get_transactions(
            wallet_address=wallet_1.address, api_key=random_api_key()
        )


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


def test_should_return_transactions_for_user(
    user_interactor: UserInteractor,
    wallet_interactor: WalletInteractor,
    transaction_interactor: TransactionInteractor,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> None:
    currency_converter.btc_to_usd = 2
    system_configuration.initial_balance = 1

    key_1 = user_interactor.create_user(random_string())
    key_2 = user_interactor.create_user(random_string())
    key_3 = user_interactor.create_user(random_string())
    wallet_1 = wallet_interactor.create_wallet(api_key=key_1)
    wallet_2 = wallet_interactor.create_wallet(api_key=key_1)
    wallet_3 = wallet_interactor.create_wallet(api_key=key_2)
    wallet_4 = wallet_interactor.create_wallet(api_key=key_3)

    # This transaction is between wallets of the same user.
    transaction_interactor.transfer(
        api_key=key_1,
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount=0.5,
    )

    transaction_interactor.transfer(
        api_key=key_1,
        source_address=wallet_2.address,
        destination_address=wallet_3.address,
        amount=0.5,
    )

    transaction_interactor.transfer(
        api_key=key_1,
        source_address=wallet_1.address,
        destination_address=wallet_4.address,
        amount=0.5,
    )

    transactions_1 = sort_transactions(
        transaction_interactor.get_user_transactions(api_key=key_1)
    )
    transactions_2 = sort_transactions(
        transaction_interactor.get_user_transactions(api_key=key_2)
    )
    transactions_3 = sort_transactions(
        transaction_interactor.get_user_transactions(api_key=key_3)
    )

    assert len(transactions_1) == 4
    assert len(transactions_2) == 1
    assert len(transactions_3) == 1

    expect_transaction(
        transaction_id=transactions_1[0].id,
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount=0.5,
    ).given(transactions_1[0]).given(transactions_1[1])

    expect_transaction(
        transaction_id=transactions_1[2].id,
        source_address=wallet_2.address,
        destination_address=wallet_3.address,
        amount=0.5,
    ).given(transactions_1[2]).given(transactions_2[0])

    expect_transaction(
        transaction_id=transactions_1[3].id,
        source_address=wallet_1.address,
        destination_address=wallet_4.address,
        amount=0.5,
    ).given(transactions_1[3]).given(transactions_3[0])


def test_should_include_transaction_fees_in_transactions_for_user(
    user_interactor: UserInteractor,
    wallet_interactor: WalletInteractor,
    transaction_interactor: TransactionInteractor,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> None:
    currency_converter.btc_to_usd = 2
    system_configuration.initial_balance = 1
    system_configuration.same_user_transfer_fee = 25

    key = user_interactor.create_user(random_string())
    wallet_1 = wallet_interactor.create_wallet(api_key=key)
    wallet_2 = wallet_interactor.create_wallet(api_key=key)

    # This transaction is between wallets of the same user.
    transaction_interactor.transfer(
        api_key=key,
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount=0.4,
    )

    transactions = sort_transactions(
        transaction_interactor.get_user_transactions(api_key=key)
    )

    assert len(transactions) == 3

    expect_transaction(
        transaction_id=transactions[0].id,
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount=0.3,
    ).given(transactions[0]).given(transactions[1])

    expect_transaction(
        source_address=wallet_1.address,
        destination_address=system_configuration.get_system_wallet_address(),
        amount=0.1,
    ).given(transactions[2])
