class InMemoryStatisticsRepository:
    def __init__(self) -> None:
        self.__total_transactions: int = 0
        self.__total_profit: float = 0

    def add_transaction(self) -> None:
        """Increments the total transaction counter of this repository by one."""
        self.__total_transactions += 1

    def get_transactions(self) -> int:
        """Returns the total number of transactions for the platform."""
        return self.__total_transactions

    def add_platform_profit(self, platform_profit: float) -> None:
        """Adds the specified amount to the total platform profit stored in this repository."""
        self.__total_profit += platform_profit

    def get_platform_profit(self) -> float:
        """Retrieves the total platform profit"""
        return self.__total_profit
