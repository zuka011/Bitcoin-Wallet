import pytest
from core import (
    InvalidApiKeyException,
    StatisticsInteractor,
    TransactionInteractor,
    UserInteractor,
    WalletInteractor,
)
from stubs.configuration import StubSystemConfiguration
from utils import random_api_key, random_string


def test_should_return_zero_transactions(
    statistics_interactor: StatisticsInteractor,
    system_configuration: StubSystemConfiguration,
) -> None:
    admin_key = random_api_key()
    system_configuration.admin_api_key = admin_key

    assert statistics_interactor.get_total_transactions(api_key=admin_key) == 0


def test_should_not_return_transactions_for_invalid_api_key(
    statistics_interactor: StatisticsInteractor,
    system_configuration: StubSystemConfiguration,
) -> None:
    with pytest.raises(InvalidApiKeyException):
        statistics_interactor.get_total_transactions(api_key=random_api_key())


def test_should_not_return_platform_profit_for_invalid_api_key(
    statistics_interactor: StatisticsInteractor,
    system_configuration: StubSystemConfiguration,
) -> None:
    with pytest.raises(InvalidApiKeyException):
        statistics_interactor.get_platform_profit(api_key=random_api_key())


def test_should_return_transactions_and_platform_profit(
    user_interactor: UserInteractor,
    wallet_interactor: WalletInteractor,
    transaction_interactor: TransactionInteractor,
    statistics_interactor: StatisticsInteractor,
    system_configuration: StubSystemConfiguration,
) -> None:
    system_configuration.initial_balance = 1
    system_configuration.same_user_transfer_fee = 0
    system_configuration.cross_user_transfer_fee = 50

    key_1 = user_interactor.create_user(random_string())
    key_2 = user_interactor.create_user(random_string())
    wallet_1 = wallet_interactor.create_wallet(api_key=key_1)
    wallet_2 = wallet_interactor.create_wallet(api_key=key_1)
    wallet_3 = wallet_interactor.create_wallet(api_key=key_2)

    transaction_interactor.transfer(
        api_key=key_1,
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount=1,
    )
    transaction_interactor.transfer(
        api_key=key_1,
        source_address=wallet_2.address,
        destination_address=wallet_3.address,
        amount=1,
    )
    transaction_interactor.transfer(
        api_key=key_2,
        source_address=wallet_3.address,
        destination_address=wallet_1.address,
        amount=1,
    )

    assert (
        statistics_interactor.get_total_transactions(
            api_key=system_configuration.admin_api_key
        )
        == 5  # Including system transactions.
    )
    assert (
        statistics_interactor.get_platform_profit(
            api_key=system_configuration.admin_api_key
        )
        == 1
    )
