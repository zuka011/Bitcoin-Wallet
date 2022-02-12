import pytest
from clients.transaction import TransactionClient
from clients.user import UserClient
from clients.wallet import WalletClient
from core import TransactionInteractor, UserInteractor, WalletInteractor
from infra import (
    InMemoryTransactionRepository,
    InMemoryUserRepository,
    InMemoryWalletRepository,
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
def currency_converter() -> StubCurrencyConverter:
    """Returns a test stub for a currency converter."""
    return StubCurrencyConverter()


@pytest.fixture
def system_configuration() -> StubSystemConfiguration:
    """Returns a test stub for a system configuration."""
    return StubSystemConfiguration()


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
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> TransactionInteractor:
    """Returns a transaction interactor, preset for testing."""
    return TransactionInteractor(
        wallet_repository=memory_wallet_repository,
        transaction_repository=memory_transaction_repository,
        currency_converter=currency_converter,
        system_configuration=system_configuration,
    )


@pytest.fixture
def test_client(
    memory_user_repository: InMemoryUserRepository,
    memory_wallet_repository: InMemoryWalletRepository,
    memory_transaction_repository: InMemoryTransactionRepository,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> TestClient:
    """Returns a preset test client."""
    return TestClient(
        setup(
            user_repository=memory_user_repository,
            wallet_repository=memory_wallet_repository,
            transaction_repository=memory_transaction_repository,
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
