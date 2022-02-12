from typing import Protocol


class IStatisticsRepository(Protocol):
    def add_transaction(self) -> None:
        """Increments the total transaction counter of this repository by one."""

    def get_transactions(self) -> int:
        """Returns the total number of transactions for the platform."""

    def add_platform_profit(self, platform_profit: float) -> None:
        """Adds the specified amount to the total platform profit stored in this repository."""

    def get_platform_profit(self) -> float:
        """Retrieves the total platform profit"""
