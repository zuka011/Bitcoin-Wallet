from typing import Any, Final

import pytest
from conftest import memory_statistics_repository, sqlite_statistics_repository
from core import IStatisticsRepository
from pytest_cases import parametrize

STATISTICS_REPOSITORIES: Final[Any] = [
    memory_statistics_repository,
    sqlite_statistics_repository,
]


@parametrize("statistics_repository", STATISTICS_REPOSITORIES)  # type: ignore
def test_should_add_transactions_to_repository(
    statistics_repository: IStatisticsRepository,
) -> None:
    statistics_repository.add_transaction()
    statistics_repository.add_transaction()
    statistics_repository.add_transaction()


@parametrize("statistics_repository", STATISTICS_REPOSITORIES)  # type: ignore
def test_should_retrieve_transactions_to_repository(
    statistics_repository: IStatisticsRepository,
) -> None:
    statistics_repository.add_transaction()
    statistics_repository.add_transaction()
    statistics_repository.add_transaction()

    assert statistics_repository.get_transactions() == 3


@parametrize("statistics_repository", STATISTICS_REPOSITORIES)  # type: ignore
def test_should_add_platform_profit_to_repository(
    statistics_repository: IStatisticsRepository,
) -> None:
    statistics_repository.add_platform_profit(platform_profit=3)
    statistics_repository.add_platform_profit(platform_profit=0.2)
    statistics_repository.add_platform_profit(platform_profit=0.0)


@parametrize("statistics_repository", STATISTICS_REPOSITORIES)  # type: ignore
def test_should_retrieve_platform_profit_to_repository(
    statistics_repository: IStatisticsRepository,
) -> None:
    statistics_repository.add_platform_profit(platform_profit=3)
    statistics_repository.add_platform_profit(platform_profit=0.2)
    statistics_repository.add_platform_profit(platform_profit=0.0)

    assert statistics_repository.get_platform_profit() == pytest.approx(3.2)
