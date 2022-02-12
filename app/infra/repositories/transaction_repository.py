from collections import defaultdict
from typing import Dict, Iterable, List

from core import TransactionEntry


class InMemoryTransactionRepository:
    def __init__(self) -> None:
        self.__transactions: Dict[str, List[TransactionEntry]] = defaultdict(lambda: [])

    def add_transaction(
        self, transaction: TransactionEntry, *, wallet_address: str
    ) -> None:
        """Adds the transaction for the specified wallet to the this repository."""
        self.__transactions[wallet_address].append(transaction)

    def get_transactions(self, *, wallet_address: str) -> Iterable[TransactionEntry]:
        """Returns all transactions associated with the specified wallet address."""
        return (transaction for transaction in self.__transactions[wallet_address])
