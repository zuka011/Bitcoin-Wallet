import pytest
from core import UserInteractor
from infra import InMemoryUserRepository, InMemoryWalletRepository
from runner.web import setup
from starlette.testclient import TestClient
from stubs.currency_converter import StubCurrencyConverter


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(setup())


@pytest.fixture
def memory_user_repository() -> InMemoryUserRepository:
    return InMemoryUserRepository()


@pytest.fixture
def memory_wallet_repository() -> InMemoryWalletRepository:
    return InMemoryWalletRepository()


@pytest.fixture
def interactor(
    memory_user_repository: InMemoryUserRepository,
    memory_wallet_repository: InMemoryWalletRepository,
) -> UserInteractor:
    return UserInteractor(
        user_repository=memory_user_repository,
        wallet_repository=memory_wallet_repository,
        currency_converter=StubCurrencyConverter(),
    )
