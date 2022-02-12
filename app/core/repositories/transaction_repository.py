from dataclasses import dataclass
from typing import Iterable, Protocol


@dataclass
class TransactionEntry:
    source_address: str
    destination_address: str
    amount: float


class ITransactionRepository(Protocol):
    def add_transaction(
        self, transaction: TransactionEntry, *, wallet_address: str
    ) -> None:
        """Adds the transaction for the specified wallet to the this repository."""

    def get_transactions(self, *, wallet_address: str) -> Iterable[TransactionEntry]:
        """Returns all transactions associated with the specified wallet address."""
