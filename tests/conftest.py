import pytest
from core import UserInteractor
from infra import InMemoryUserRepository
from runner.web import setup
from starlette.testclient import TestClient


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(setup())


@pytest.fixture
def repository() -> InMemoryUserRepository:
    return InMemoryUserRepository()


@pytest.fixture
def interactor(repository: InMemoryUserRepository) -> UserInteractor:
    return UserInteractor(user_repository=repository)
