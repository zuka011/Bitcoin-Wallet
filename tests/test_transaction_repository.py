from datetime import datetime
from typing import Any, Final

from conftest import (
    memory_transaction_repository,
    memory_wallet_repository,
    sqlite_transaction_repository,
    sqlite_wallet_repository,
)
from core import (
    Currency,
    ITransactionRepository,
    IWalletRepository,
    TransactionEntry,
    WalletEntry,
)
from infra import SqliteUserRepository
from pytest_cases import parametrize
from utils import random_api_key, random_string, sort_transaction_entries

TRANSACTION_REPOSITORIES: Final[Any] = [
    memory_transaction_repository,
    sqlite_transaction_repository,
]
WALLET_REPOSITORIES: Final[Any] = [memory_wallet_repository, sqlite_wallet_repository]


@parametrize(
    "transaction_repository, wallet_repository",
    zip(TRANSACTION_REPOSITORIES, WALLET_REPOSITORIES),
)  # type: ignore
def test_should_add_transactions_to_repository(
    transaction_repository: ITransactionRepository,
    wallet_repository: IWalletRepository,
    sqlite_user_repository: SqliteUserRepository,
) -> None:
    key_1 = random_api_key()
    key_2 = random_api_key()
    wallet_1 = WalletEntry(address=random_string(), balance=1.5, currency=Currency.BTC)
    wallet_2 = WalletEntry(address=random_string(), balance=5.0, currency=Currency.BTC)
    wallet_3 = WalletEntry(address=random_string(), balance=7.9, currency=Currency.BTC)

    transaction_1 = TransactionEntry(
        id=random_string(),
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount=0.75,
        timestamp=datetime.now(),
    )
    transaction_2 = TransactionEntry(
        id=random_string(),
        source_address=wallet_2.address,
        destination_address=wallet_3.address,
        amount=0.75,
        timestamp=datetime.now(),
    )

    sqlite_user_repository.add_user(api_key=key_1, username=random_string())
    sqlite_user_repository.add_user(api_key=key_2, username=random_string())
    wallet_repository.add_wallet(wallet=wallet_1, api_key=key_1)
    wallet_repository.add_wallet(wallet=wallet_2, api_key=key_1)
    wallet_repository.add_wallet(wallet=wallet_3, api_key=key_2)

    transaction_repository.add_transaction(
        transaction_1, wallet_address=wallet_1.address
    )
    transaction_repository.add_transaction(
        transaction_1, wallet_address=wallet_2.address
    )
    transaction_repository.add_transaction(
        transaction_2, wallet_address=wallet_2.address
    )
    transaction_repository.add_transaction(
        transaction_2, wallet_address=wallet_3.address
    )


@parametrize(
    "transaction_repository, wallet_repository",
    zip(TRANSACTION_REPOSITORIES, WALLET_REPOSITORIES),
)  # type: ignore
def test_should_retrieve_transactions_for_wallets(
    transaction_repository: ITransactionRepository,
    wallet_repository: IWalletRepository,
    sqlite_user_repository: SqliteUserRepository,
) -> None:
    key_1 = random_api_key()
    key_2 = random_api_key()
    wallet_1 = WalletEntry(address=random_string(), balance=1.5, currency=Currency.BTC)
    wallet_2 = WalletEntry(address=random_string(), balance=5.0, currency=Currency.BTC)
    wallet_3 = WalletEntry(address=random_string(), balance=7.9, currency=Currency.BTC)

    transaction_1 = TransactionEntry(
        id=random_string(),
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount=0.75,
        timestamp=datetime.now(),
    )
    transaction_2 = TransactionEntry(
        id=random_string(),
        source_address=wallet_2.address,
        destination_address=wallet_3.address,
        amount=0.75,
        timestamp=datetime.now(),
    )

    sqlite_user_repository.add_user(api_key=key_1, username=random_string())
    sqlite_user_repository.add_user(api_key=key_2, username=random_string())
    wallet_repository.add_wallet(wallet=wallet_1, api_key=key_1)
    wallet_repository.add_wallet(wallet=wallet_2, api_key=key_1)
    wallet_repository.add_wallet(wallet=wallet_3, api_key=key_2)

    transaction_repository.add_transaction(
        transaction_1, wallet_address=wallet_1.address
    )
    transaction_repository.add_transaction(
        transaction_1, wallet_address=wallet_2.address
    )
    transaction_repository.add_transaction(
        transaction_2, wallet_address=wallet_2.address
    )
    transaction_repository.add_transaction(
        transaction_2, wallet_address=wallet_3.address
    )

    assert sort_transaction_entries(
        transaction_repository.get_transactions(wallet_address=wallet_1.address)
    ) == [transaction_1]
    assert sort_transaction_entries(
        transaction_repository.get_transactions(wallet_address=wallet_2.address)
    ) == [transaction_1, transaction_2]
    assert sort_transaction_entries(
        transaction_repository.get_transactions(wallet_address=wallet_3.address)
    ) == [transaction_2]


@parametrize(
    "transaction_repository, wallet_repository",
    zip(TRANSACTION_REPOSITORIES, WALLET_REPOSITORIES),
)  # type: ignore
def test_should_retrieve_transactions_for_users(
    transaction_repository: ITransactionRepository,
    wallet_repository: IWalletRepository,
    sqlite_user_repository: SqliteUserRepository,
) -> None:
    key_1 = random_api_key()
    key_2 = random_api_key()
    wallet_1 = WalletEntry(address=random_string(), balance=1.5, currency=Currency.BTC)
    wallet_2 = WalletEntry(address=random_string(), balance=5.0, currency=Currency.BTC)
    wallet_3 = WalletEntry(address=random_string(), balance=7.9, currency=Currency.BTC)

    transaction_1 = TransactionEntry(
        id=random_string(),
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount=0.75,
        timestamp=datetime.now(),
    )
    transaction_2 = TransactionEntry(
        id=random_string(),
        source_address=wallet_2.address,
        destination_address=wallet_3.address,
        amount=0.75,
        timestamp=datetime.now(),
    )

    sqlite_user_repository.add_user(api_key=key_1, username=random_string())
    sqlite_user_repository.add_user(api_key=key_2, username=random_string())
    wallet_repository.add_wallet(wallet=wallet_1, api_key=key_1)
    wallet_repository.add_wallet(wallet=wallet_2, api_key=key_1)
    wallet_repository.add_wallet(wallet=wallet_3, api_key=key_2)

    transaction_repository.add_transaction(
        transaction_1, wallet_address=wallet_1.address
    )
    transaction_repository.add_transaction(
        transaction_1, wallet_address=wallet_2.address
    )
    transaction_repository.add_transaction(
        transaction_2, wallet_address=wallet_2.address
    )
    transaction_repository.add_transaction(
        transaction_2, wallet_address=wallet_3.address
    )

    assert sort_transaction_entries(
        transaction_repository.get_user_transactions(api_key=key_1)
    ) == [transaction_1, transaction_1, transaction_2]
    assert sort_transaction_entries(
        transaction_repository.get_user_transactions(api_key=key_2)
    ) == [transaction_2]
