from dataclasses import dataclass
from typing import Protocol

from core.currencies import Currency


@dataclass(frozen=True)
class WalletEntry:
    address: str
    balance: float
    currency: Currency


class IWalletRepository(Protocol):
    def add_wallet(self, wallet: WalletEntry, *, api_key: str) -> None:
        """Adds a wallet to this repository for the user with the specified API key."""

    def get_wallet(self, *, wallet_address: str) -> WalletEntry:
        """Returns the wallet corresponding with the specified address."""

    def update_wallet(self, wallet: WalletEntry, *, wallet_address: str) -> None:
        """Updates the wallet with the specified address."""

    def get_wallet_count(self, *, api_key: str) -> int:
        """Returns the number of wallets belonging to the user with the specified API key."""

    def is_wallet_owner(self, *, wallet_address: str, api_key: str) -> bool:
        """Returns true if wallet belongs to user with the specified API key."""

    def get_wallet_owner(self, *, wallet_address: str) -> str:
        """Returns the API key of the owner of the specified wallet."""
