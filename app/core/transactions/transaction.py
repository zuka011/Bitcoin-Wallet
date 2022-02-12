from datetime import datetime

from core.repositories import TransactionEntry


class Transaction:
    def __init__(self, *, transaction_entry: TransactionEntry) -> None:
        self.__transaction_entry = transaction_entry

    @property
    def id(self) -> str:
        """Returns the unique ID of this transaction."""
        return self.__transaction_entry.id

    @property
    def source_address(self) -> str:
        """Returns the source wallet address in this transaction."""
        return self.__transaction_entry.source_address

    @property
    def destination_address(self) -> str:
        """Returns the destination wallet address in this transaction."""
        return self.__transaction_entry.destination_address

    @property
    def amount(self) -> float:
        """Returns the transfer amount."""
        return self.__transaction_entry.amount

    @property
    def timestamp(self) -> datetime:
        """Returns the timestamp of the transfer."""
        return self.__transaction_entry.timestamp
