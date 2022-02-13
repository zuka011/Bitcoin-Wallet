from collections import defaultdict
from typing import Dict, List

from core.repositories import WalletEntry


class InMemoryWalletRepository:
    def __init__(self) -> None:
        self.__wallets_by_api_key: Dict[str, List[WalletEntry]] = defaultdict(
            lambda: []
        )
        self.__api_keys_by_wallet_address: Dict[str, str] = {}
        self.__wallet_by_address: Dict[str, WalletEntry] = {}

    def add_wallet(self, wallet: WalletEntry, *, api_key: str) -> None:
        """Adds a wallet for the user with the specified API key."""
        self.__wallets_by_api_key[api_key].append(wallet)
        self.__wallet_by_address[wallet.address] = wallet
        self.__api_keys_by_wallet_address[wallet.address] = api_key

    def has_wallet(self, *, wallet_address: str) -> bool:
        """Returns the wallet corresponding with the specified address."""
        return wallet_address in self.__wallet_by_address

    def get_wallet(self, *, wallet_address: str) -> WalletEntry:
        """Returns the wallet corresponding with the specified address."""
        assert (
            wallet_address in self.__wallet_by_address
        ), f"A wallet with the address {wallet_address} does not exist."

        return self.__wallet_by_address[wallet_address]

    def update_wallet(self, wallet: WalletEntry, *, wallet_address: str) -> None:
        """Updates the wallet with the specified address."""
        assert (
            wallet_address in self.__wallet_by_address
        ), f"A wallet with the address {wallet_address} does not exist."
        assert (
            wallet_address == wallet.address
        ), "The specified wallet address differs from the one in the entry."

        self.__wallet_by_address[wallet_address] = wallet

    def get_wallet_count(self, *, api_key: str) -> int:
        """Returns the number of wallets belonging to the user with the specified API key."""
        return len(self.__wallets_by_api_key[api_key])

    def is_wallet_owner(self, *, wallet_address: str, api_key: str) -> bool:
        """Returns true if the wallet belongs to the user with the specified API key."""
        assert (
            wallet_address in self.__api_keys_by_wallet_address
        ), f"A wallet with the address {wallet_address} does not exist."

        return self.__api_keys_by_wallet_address[wallet_address] == api_key

    def get_wallet_owner(self, *, wallet_address: str) -> str:
        """Returns the API key of the owner of the specified wallet."""
        assert (
            wallet_address in self.__api_keys_by_wallet_address
        ), f"A wallet with the address {wallet_address} does not exist."

        return self.__api_keys_by_wallet_address[wallet_address]
