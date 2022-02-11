import pytest
from core import UserInteractor, WalletInteractor
from infra import InMemoryUserRepository
from runner.web import setup
from starlette.testclient import TestClient
from stubs.currency_converter import StubCurrencyConverter


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(setup())


@pytest.fixture
def repository() -> InMemoryUserRepository:
    return InMemoryUserRepository()


@pytest.fixture
def currency_converter() -> StubCurrencyConverter:
    return StubCurrencyConverter()


@pytest.fixture
def user_interactor(repository: InMemoryUserRepository) -> UserInteractor:
    return UserInteractor(user_repository=repository)


@pytest.fixture
def wallet_interactor(
    repository: InMemoryUserRepository, currency_converter: StubCurrencyConverter
) -> WalletInteractor:
    return WalletInteractor(
        user_repository=repository, currency_converter=currency_converter
    )
