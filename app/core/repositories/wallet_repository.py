from typing import Protocol


class IWalletRepository(Protocol):
    def add_wallet(self, *, api_key: str) -> None:
        """Adds a wallet for the user with the specified API key."""

    def get_wallet_count(self, *, api_key: str) -> int:
        """Returns the number of wallets belonging to the user with the specified API key."""
