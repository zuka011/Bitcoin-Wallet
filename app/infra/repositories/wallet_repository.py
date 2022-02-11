from collections import defaultdict
from typing import Dict


class InMemoryWalletRepository:
    def __init__(self) -> None:
        self.__wallet_count: Dict[str, int] = defaultdict(lambda: 0)

    def add_wallet(self, *, api_key: str) -> None:
        """Adds a wallet for the user with the specified API key."""
        self.__wallet_count[api_key] += 1

    def get_wallet_count(self, *, api_key: str) -> int:
        """Returns the number of wallets belonging to the user with the specified API key."""
        return self.__wallet_count[api_key]
