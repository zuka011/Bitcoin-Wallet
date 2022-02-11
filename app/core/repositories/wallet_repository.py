from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Wallet:
    address: str
    balance_btc: float
    balance_usd: float


class IWalletRepository(Protocol):
    def add_wallet(self, wallet: Wallet, *, api_key: str) -> None:
        """Adds a wallet to this repository for the user with the specified API key."""

    def get_wallet(self, *, wallet_address: str) -> Wallet:
        """Returns the wallet corresponding with the specified address."""

    def update_wallet(self, wallet: Wallet, *, wallet_address: str) -> None:
        """Updates the wallet with the specified address."""

    def get_wallet_count(self, *, api_key: str) -> int:
        """Returns the number of wallets belonging to the user with the specified API key."""
