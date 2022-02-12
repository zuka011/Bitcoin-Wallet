from dataclasses import dataclass

from infra.sqlite.sqlite import SqliteRepository


@dataclass
class StatisticsEntry:
    transaction_count: int
    total_profit: float


class SqliteStatisticsRepository(SqliteRepository):
    def add_transaction(self) -> None:
        """Increments the total transaction counter of this repository by one."""
        transactions = self.get_transactions()
        self.update(
            "UPDATE statistics SET transaction_count=:transaction_count",  # noqa: It's a weird table, don't ask.
            parameters={"transaction_count": transactions + 1},
        )

    def get_transactions(self) -> int:
        """Returns the total number of transactions for the platform."""
        return self.__get_data().transaction_count

    def add_platform_profit(self, platform_profit: float) -> None:
        """Adds the specified amount to the total platform profit stored in this repository."""
        total_profit = self.get_platform_profit()
        self.update(
            "UPDATE statistics SET total_profit=:total_profit",  # noqa: It's a weird table, don't ask.
            parameters={"total_profit": total_profit + platform_profit},
        )

    def get_platform_profit(self) -> float:
        """Retrieves the total platform profit"""
        return self.__get_data().total_profit

    def __get_data(self) -> StatisticsEntry:
        """Retrieves the only row from the statistics table, or creates one if it doesn't exist."""
        result = self.query(
            "SELECT transaction_count, total_profit FROM statistics"
        ).fetchone()
        if result is None:
            self.update(
                "INSERT INTO statistics (transaction_count, total_profit) VALUES (0, 0)"
            )
            return StatisticsEntry(transaction_count=0, total_profit=0)
        else:
            return StatisticsEntry(
                transaction_count=int(result[0]), total_profit=float(result[1])
            )
