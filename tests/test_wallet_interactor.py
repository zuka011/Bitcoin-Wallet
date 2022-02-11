import pytest
from conftest import DEFAULT_INITIAL_BALANCE
from core import (
    InvalidApiKeyException,
    InvalidWalletRequestException,
    UserInteractor,
    WalletApiKeyValidator,
    WalletInteractor,
    WalletLimitValidator,
)
from infra import (
    CoinLayerCurrencyConverter,
    InMemoryUserRepository,
    InMemoryWalletRepository,
)
from stubs.currency_converter import StubCurrencyConverter
from utils import random_string


def test_should_create_wallet_for_user(
    user_interactor: UserInteractor, wallet_interactor: WalletInteractor
) -> None:
    key = user_interactor.create_user(random_string())
    assert wallet_interactor.create_wallet(key) is not None


def test_should_not_create_wallet_for_invalid_user(
    memory_user_repository: InMemoryUserRepository,
    memory_wallet_repository: InMemoryWalletRepository,
    currency_converter: StubCurrencyConverter,
) -> None:
    key = random_string()

    wallet_interactor = WalletInteractor(
        user_repository=memory_user_repository,
        wallet_repository=memory_wallet_repository,
        currency_converter=currency_converter,
        initial_balance=DEFAULT_INITIAL_BALANCE,
        wallet_validators=[
            WalletApiKeyValidator(user_repository=memory_user_repository)
        ],
    )

    with pytest.raises(InvalidApiKeyException):
        wallet_interactor.create_wallet(key)


def test_should_not_create_too_many_wallets(
    user_interactor: UserInteractor,
    memory_user_repository: InMemoryUserRepository,
    memory_wallet_repository: InMemoryWalletRepository,
    currency_converter: StubCurrencyConverter,
) -> None:
    wallet_interactor = WalletInteractor(
        user_repository=memory_user_repository,
        wallet_repository=memory_wallet_repository,
        currency_converter=currency_converter,
        initial_balance=DEFAULT_INITIAL_BALANCE,
        wallet_validators=[
            WalletLimitValidator(
                wallet_limit=3, wallet_repository=memory_wallet_repository
            )
        ],
    )

    key = user_interactor.create_user("Bla bla user")
    wallet_interactor.create_wallet(key)
    wallet_interactor.create_wallet(key)
    wallet_interactor.create_wallet(key)

    with pytest.raises(InvalidWalletRequestException):
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
    user_interactor: UserInteractor,
    memory_user_repository: InMemoryUserRepository,
    memory_wallet_repository: InMemoryWalletRepository,
) -> None:
    wallet_interactor = WalletInteractor(
        user_repository=memory_user_repository,
        wallet_repository=memory_wallet_repository,
        currency_converter=StubCurrencyConverter(2),
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
