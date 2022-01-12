import pytest
from runner.web import setup
from starlette.testclient import TestClient


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(setup())
