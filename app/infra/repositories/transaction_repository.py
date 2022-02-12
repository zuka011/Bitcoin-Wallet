from collections import defaultdict
from typing import Dict, Iterable, List

from core import IWalletRepository, TransactionEntry


class InMemoryTransactionRepository:
    def __init__(self, *, wallet_repository: IWalletRepository) -> None:
        self.__wallet_repository = wallet_repository
        self.__transactions_by_address: Dict[str, List[TransactionEntry]] = defaultdict(
            lambda: []
        )
        self.__transactions_by_key: Dict[str, List[TransactionEntry]] = defaultdict(
            lambda: []
        )

    def add_transaction(
        self, transaction: TransactionEntry, *, wallet_address: str
    ) -> None:
        """Adds the transaction for the specified wallet to the this repository."""
        api_key = self.__wallet_repository.get_wallet_owner(
            wallet_address=wallet_address
        )

        self.__transactions_by_address[wallet_address].append(transaction)
        self.__transactions_by_key[api_key].append(transaction)

    def get_transactions(self, *, wallet_address: str) -> Iterable[TransactionEntry]:
        """Returns all transactions associated with the specified wallet address."""
        return (
            transaction
            for transaction in self.__transactions_by_address[wallet_address]
        )

    def get_user_transactions(self, *, api_key: str) -> Iterable[TransactionEntry]:
        """Returns all transactions associated with the user with the specified API key."""
        return (transaction for transaction in self.__transactions_by_key[api_key])
