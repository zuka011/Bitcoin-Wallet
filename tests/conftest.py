from typing import Final

import pytest
from core import UserInteractor, WalletInteractor
from infra import InMemoryUserRepository, InMemoryWalletRepository
from runner.web import setup
from starlette.testclient import TestClient
from stubs.currency_converter import StubCurrencyConverter

DEFAULT_INITIAL_BALANCE: Final[float] = 1


@pytest.fixture
def test_client() -> TestClient:
    """Returns a preset test client."""
    return TestClient(setup())


@pytest.fixture
def memory_user_repository() -> InMemoryUserRepository:
    """Returns an in-memory implementation of a user repository."""
    return InMemoryUserRepository()


@pytest.fixture
def memory_wallet_repository() -> InMemoryWalletRepository:
    """Returns an in-memory implementation of a wallet repository."""
    return InMemoryWalletRepository()


@pytest.fixture
def currency_converter() -> StubCurrencyConverter:
    """Returns a test stub for a currency converter."""
    return StubCurrencyConverter()


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
) -> WalletInteractor:
    """Returns a wallet interactor, preset for testing."""
    return WalletInteractor(
        user_repository=memory_user_repository,
        wallet_repository=memory_wallet_repository,
        currency_converter=currency_converter,
        initial_balance=DEFAULT_INITIAL_BALANCE,
    )
