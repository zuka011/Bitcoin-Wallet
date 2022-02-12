import pytest
from core import (
    Currency,
    InvalidApiKeyException,
    InvalidWalletRequestException,
    TransactionInteractor,
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
from stubs.configuration import StubSystemConfiguration
from stubs.currency_converter import StubCurrencyConverter
from utils import random_api_key, random_string


def test_should_create_wallet_for_user(
    user_interactor: UserInteractor, wallet_interactor: WalletInteractor
) -> None:
    key = user_interactor.create_user(random_string())
    assert wallet_interactor.create_wallet(key) is not None


def test_should_not_create_wallet_for_invalid_user(
    memory_user_repository: InMemoryUserRepository,
    memory_wallet_repository: InMemoryWalletRepository,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> None:
    key = random_string()

    wallet_interactor = WalletInteractor(
        user_repository=memory_user_repository,
        wallet_repository=memory_wallet_repository,
        currency_converter=currency_converter,
        system_configuration=system_configuration,
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
    system_configuration: StubSystemConfiguration,
) -> None:
    wallet_interactor = WalletInteractor(
        user_repository=memory_user_repository,
        wallet_repository=memory_wallet_repository,
        currency_converter=currency_converter,
        system_configuration=system_configuration,
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
    wallet_interactor: WalletInteractor,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> None:
    currency_converter.btc_to_usd = 2
    system_configuration.initial_balance = 1

    key = user_interactor.create_user(random_string())
    wallet = wallet_interactor.create_wallet(key)
    assert wallet.get_balance(currency=Currency.BTC) == 1
    assert wallet.get_balance(currency=Currency.USD) == 2


def test_should_retrieve_wallet(
    user_interactor: UserInteractor, wallet_interactor: WalletInteractor
) -> None:
    key = user_interactor.create_user(random_string())
    wallet = wallet_interactor.create_wallet(api_key=key)

    assert wallet_interactor.get_wallet(address=wallet.address, api_key=key) == wallet


def test_should_not_retrieve_wallet_with_incorrect_api_key(
    user_interactor: UserInteractor, wallet_interactor: WalletInteractor
) -> None:
    key = user_interactor.create_user(random_string())
    wallet = wallet_interactor.create_wallet(api_key=key)

    with pytest.raises(InvalidApiKeyException):
        wallet_interactor.get_wallet(address=wallet.address, api_key=random_api_key())


def test_should_get_real_time_balance() -> None:
    assert (
        CoinLayerCurrencyConverter.convert(5, source=Currency.BTC, target=Currency.USD)
        is not None
    )


def test_should_return_correct_funds_after_exchange_rate_changes(
    user_interactor: UserInteractor,
    wallet_interactor: WalletInteractor,
    transaction_interactor: TransactionInteractor,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> None:
    currency_converter.btc_to_usd = 2
    system_configuration.initial_balance = 10
    system_configuration.same_user_transfer_fee = 0

    key = user_interactor.create_user("User")
    address = wallet_interactor.create_wallet(key).address

    currency_converter.btc_to_usd = 3

    wallet = wallet_interactor.get_wallet(address=address, api_key=key)

    assert wallet.get_balance(currency=Currency.BTC) == 10
    assert wallet.get_balance(currency=Currency.USD) == 30
