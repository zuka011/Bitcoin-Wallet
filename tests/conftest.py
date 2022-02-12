from typing import Iterator

import pytest
from clients.statistics import StatisticsClient
from clients.transaction import TransactionClient
from clients.user import UserClient
from clients.wallet import WalletClient
from core import (
    StatisticsInteractor,
    TransactionInteractor,
    UserInteractor,
    WalletInteractor,
)
from infra import (
    InMemoryConnectionFactory,
    InMemoryStatisticsRepository,
    InMemoryTransactionRepository,
    InMemoryUserRepository,
    InMemoryWalletRepository,
    SqliteUserRepository,
    SqliteWalletRepository,
)
from runner.web import setup
from starlette.testclient import TestClient
from stubs.configuration import StubSystemConfiguration
from stubs.currency_converter import StubCurrencyConverter


@pytest.fixture
def memory_user_repository() -> InMemoryUserRepository:
    """Returns an in-memory implementation of a user repository."""
    return InMemoryUserRepository()


@pytest.fixture
def memory_wallet_repository() -> InMemoryWalletRepository:
    """Returns an in-memory implementation of a wallet repository."""
    return InMemoryWalletRepository()


@pytest.fixture
def memory_transaction_repository(
    memory_wallet_repository: InMemoryWalletRepository,
) -> InMemoryTransactionRepository:
    """Returns an in-memory implementation of a transaction repository."""
    return InMemoryTransactionRepository(wallet_repository=memory_wallet_repository)


@pytest.fixture
def memory_statistics_repository() -> InMemoryStatisticsRepository:
    """Returns an in-memory implementation of a statistics repository."""
    return InMemoryStatisticsRepository()


@pytest.fixture
def currency_converter() -> StubCurrencyConverter:
    """Returns a test stub for a currency converter."""
    return StubCurrencyConverter()


@pytest.fixture
def system_configuration() -> StubSystemConfiguration:
    """Returns a test stub for a system configuration."""
    return StubSystemConfiguration()


@pytest.fixture
def memory_connection_factory() -> InMemoryConnectionFactory:
    """Returns an in-memory SQLite connection factory."""
    return InMemoryConnectionFactory()


@pytest.fixture
def sqlite_user_repository(
    memory_connection_factory: InMemoryConnectionFactory,
) -> Iterator[SqliteUserRepository]:
    """Returns an in-memory SQLite user repository."""
    with SqliteUserRepository(
        connection_factory=memory_connection_factory,
        init_files=["data_base/users.sql"],
    ) as repository:
        yield repository


@pytest.fixture
def sqlite_wallet_repository(
    memory_connection_factory: InMemoryConnectionFactory,
) -> Iterator[SqliteWalletRepository]:
    """Returns an in-memory SQLite user repository."""
    with SqliteWalletRepository(
        connection_factory=memory_connection_factory,
        init_files=["data_base/users.sql", "data_base/wallets.sql"],
    ) as repository:
        yield repository


@pytest.fixture
def user_interactor(memory_user_repository: InMemoryUserRepository) -> UserInteractor:
    """Returns a user interactor, preset for testing."""
    return UserInteractor(
        user_repository=memory_user_repository,
    )


@pytest.fixture
def wallet_interactor(
    memory_user_repository: InMemoryUserRepository,
    memory_wallet_repository: InMemoryWalletRepository,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> WalletInteractor:
    """Returns a wallet interactor, preset for testing."""
    return WalletInteractor(
        user_repository=memory_user_repository,
        wallet_repository=memory_wallet_repository,
        currency_converter=currency_converter,
        system_configuration=system_configuration,
    )


@pytest.fixture
def transaction_interactor(
    memory_wallet_repository: InMemoryWalletRepository,
    memory_transaction_repository: InMemoryTransactionRepository,
    memory_statistics_repository: InMemoryStatisticsRepository,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> TransactionInteractor:
    """Returns a transaction interactor, preset for testing."""
    return TransactionInteractor(
        wallet_repository=memory_wallet_repository,
        transaction_repository=memory_transaction_repository,
        statistics_repository=memory_statistics_repository,
        currency_converter=currency_converter,
        system_configuration=system_configuration,
    )


@pytest.fixture
def statistics_interactor(
    memory_statistics_repository: InMemoryStatisticsRepository,
    system_configuration: StubSystemConfiguration,
) -> StatisticsInteractor:
    """Returns a statistics interactor, preset for testing."""
    return StatisticsInteractor(
        statistics_repository=memory_statistics_repository,
        system_configuration=system_configuration,
    )


@pytest.fixture
def test_client(
    memory_user_repository: InMemoryUserRepository,
    memory_wallet_repository: InMemoryWalletRepository,
    memory_transaction_repository: InMemoryTransactionRepository,
    memory_statistics_repository: InMemoryStatisticsRepository,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> TestClient:
    """Returns a preset test client."""
    return TestClient(
        setup(
            user_repository=memory_user_repository,
            wallet_repository=memory_wallet_repository,
            transaction_repository=memory_transaction_repository,
            statistics_repository=memory_statistics_repository,
            currency_converter=currency_converter,
            system_configuration=system_configuration,
        )
    )


@pytest.fixture
def user_client(test_client: TestClient) -> UserClient:
    """Returns a convenient test client for the User API."""
    return UserClient(test_client)


@pytest.fixture
def wallet_client(test_client: TestClient) -> WalletClient:
    """Returns a convenient test client for the Wallet API."""
    return WalletClient(test_client)


@pytest.fixture
def transaction_client(test_client: TestClient) -> TransactionClient:
    """Returns a convenient test client for the Transaction API."""
    return TransactionClient(test_client)


@pytest.fixture
def statistics_client(test_client: TestClient) -> StatisticsClient:
    """Returns a convenient test client for the Statistics API."""
    return StatisticsClient(test_client)
