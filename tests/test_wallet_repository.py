from typing import Any, Final

from conftest import memory_wallet_repository, sqlite_wallet_repository
from core import Currency, IWalletRepository, WalletEntry
from infra import SqliteUserRepository
from pytest_cases import parametrize
from utils import random_api_key, random_string

WALLET_REPOSITORIES: Final[Any] = [memory_wallet_repository, sqlite_wallet_repository]


@parametrize("wallet_repository", WALLET_REPOSITORIES)  # type: ignore
def test_should_add_wallets_to_repository(
    wallet_repository: IWalletRepository, sqlite_user_repository: SqliteUserRepository
) -> None:
    key = random_api_key()

    sqlite_user_repository.add_user(api_key=key, username=random_string())
    wallet_repository.add_wallet(
        wallet=WalletEntry(address=random_string(), balance=1.5, currency=Currency.BTC),
        api_key=key,
    )
    wallet_repository.add_wallet(
        wallet=WalletEntry(address=random_string(), balance=4.5, currency=Currency.BTC),
        api_key=key,
    )
    wallet_repository.add_wallet(
        wallet=WalletEntry(address=random_string(), balance=5.0, currency=Currency.BTC),
        api_key=key,
    )


@parametrize("wallet_repository", WALLET_REPOSITORIES)  # type: ignore
def test_should_retrieve_wallets_from_repository(
    wallet_repository: IWalletRepository, sqlite_user_repository: SqliteUserRepository
) -> None:
    key = random_api_key()
    wallet_1 = WalletEntry(address=random_string(), balance=1.5, currency=Currency.BTC)
    wallet_2 = WalletEntry(address=random_string(), balance=5.0, currency=Currency.USD)

    sqlite_user_repository.add_user(api_key=key, username=random_string())
    wallet_repository.add_wallet(wallet=wallet_1, api_key=key)
    wallet_repository.add_wallet(wallet=wallet_2, api_key=key)

    assert wallet_repository.get_wallet(wallet_address=wallet_1.address) == wallet_1
    assert wallet_repository.get_wallet(wallet_address=wallet_2.address) == wallet_2


@parametrize("wallet_repository", WALLET_REPOSITORIES)  # type: ignore
def test_should_update_wallet(
    wallet_repository: IWalletRepository, sqlite_user_repository: SqliteUserRepository
) -> None:
    key = random_api_key()
    address = random_string()
    wallet_1 = WalletEntry(address=address, balance=1.5, currency=Currency.BTC)
    wallet_2 = WalletEntry(address=address, balance=5.0, currency=Currency.USD)

    sqlite_user_repository.add_user(api_key=key, username=random_string())
    wallet_repository.add_wallet(wallet=wallet_1, api_key=key)
    wallet_repository.update_wallet(wallet=wallet_2, wallet_address=address)

    assert wallet_repository.get_wallet(wallet_address=address) == wallet_2


@parametrize("wallet_repository", WALLET_REPOSITORIES)  # type: ignore
def test_should_retrieve_wallet_count_for_user(
    wallet_repository: IWalletRepository, sqlite_user_repository: SqliteUserRepository
) -> None:
    key = random_api_key()
    wallet_1 = WalletEntry(address=random_string(), balance=1.5, currency=Currency.BTC)
    wallet_2 = WalletEntry(address=random_string(), balance=5.0, currency=Currency.USD)

    sqlite_user_repository.add_user(api_key=key, username=random_string())
    wallet_repository.add_wallet(wallet=wallet_1, api_key=key)
    wallet_repository.add_wallet(wallet=wallet_2, api_key=key)

    assert wallet_repository.get_wallet_count(api_key=key) == 2


@parametrize("wallet_repository", WALLET_REPOSITORIES)  # type: ignore
def test_should_check_wallet_owner(
    wallet_repository: IWalletRepository, sqlite_user_repository: SqliteUserRepository
) -> None:
    key = random_api_key()
    other_key = random_api_key()
    wallet_1 = WalletEntry(address=random_string(), balance=5.1, currency=Currency.BTC)
    wallet_2 = WalletEntry(address=random_string(), balance=5.5, currency=Currency.USD)
    wallet_3 = WalletEntry(address=random_string(), balance=0.5, currency=Currency.USD)

    sqlite_user_repository.add_user(api_key=key, username=random_string())
    sqlite_user_repository.add_user(api_key=other_key, username=random_string())
    wallet_repository.add_wallet(wallet=wallet_1, api_key=key)
    wallet_repository.add_wallet(wallet=wallet_2, api_key=key)
    wallet_repository.add_wallet(wallet=wallet_3, api_key=other_key)

    assert (
        wallet_repository.is_wallet_owner(wallet_address=wallet_1.address, api_key=key)
        is True
    )
    assert (
        wallet_repository.is_wallet_owner(wallet_address=wallet_2.address, api_key=key)
        is True
    )
    assert (
        wallet_repository.is_wallet_owner(wallet_address=wallet_3.address, api_key=key)
        is False
    )


@parametrize("wallet_repository", WALLET_REPOSITORIES)  # type: ignore
def test_should_retrieve_wallet_owner(
    wallet_repository: IWalletRepository, sqlite_user_repository: SqliteUserRepository
) -> None:
    key_1 = random_api_key()
    key_2 = random_api_key()
    wallet_1 = WalletEntry(address=random_string(), balance=5.1, currency=Currency.BTC)
    wallet_2 = WalletEntry(address=random_string(), balance=0.5, currency=Currency.USD)

    sqlite_user_repository.add_user(api_key=key_1, username=random_string())
    sqlite_user_repository.add_user(api_key=key_2, username=random_string())
    wallet_repository.add_wallet(wallet=wallet_1, api_key=key_1)
    wallet_repository.add_wallet(wallet=wallet_2, api_key=key_2)

    assert wallet_repository.get_wallet_owner(wallet_address=wallet_1.address) == key_1
    assert wallet_repository.get_wallet_owner(wallet_address=wallet_2.address) == key_2
