import pytest
from core import UserInteractor
from infra import InMemoryUserRepository
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
def interactor(memory_user_repository: InMemoryUserRepository) -> UserInteractor:
    return UserInteractor(
        user_repository=memory_user_repository,
        currency_converter=StubCurrencyConverter(),
    )
