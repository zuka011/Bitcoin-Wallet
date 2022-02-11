from collections import defaultdict
from typing import Dict, List

from core.repositories import Wallet


class InMemoryWalletRepository:
    def __init__(self) -> None:
        self.__wallets_by_api_key: Dict[str, List[Wallet]] = defaultdict(lambda: [])
        self.__wallet_by_address: Dict[str, Wallet] = {}

    def add_wallet(self, wallet: Wallet, *, api_key: str) -> None:
        """Adds a wallet for the user with the specified API key."""
        self.__wallets_by_api_key[api_key].append(wallet)
        self.__wallet_by_address[wallet.address] = wallet

    def get_wallet(self, *, wallet_address: str) -> Wallet:
        """Returns the wallet corresponding with the specified address."""
        assert (
            wallet_address in self.__wallet_by_address
        ), f"A wallet with the address {wallet_address} does not exist."

        return self.__wallet_by_address[wallet_address]

    def update_wallet(self, wallet: Wallet, *, wallet_address: str) -> None:
        """Updates the wallet with the specified address."""
        assert (
            wallet_address in self.__wallet_by_address
        ), f"A wallet with the address {wallet_address} does not exist."

        self.__wallet_by_address[wallet_address] = wallet

    def get_wallet_count(self, *, api_key: str) -> int:
        """Returns the number of wallets belonging to the user with the specified API key."""
        return len(self.__wallets_by_api_key[api_key])

    def is_wallet_owner(self, *, wallet_address: str, api_key: str) -> bool:
        """Returns true if wallet belongs to user with the specified API key."""
        return any(
            wallet.address == wallet_address
            for wallet in self.__wallets_by_api_key[api_key]
        )
