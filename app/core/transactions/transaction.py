from core.repositories import TransactionEntry


class Transaction:
    def __init__(self, *, transaction_entry: TransactionEntry) -> None:
        self.__transaction_entry = transaction_entry

    @property
    def source_address(self) -> str:
        return self.__transaction_entry.source_address

    @property
    def destination_address(self) -> str:
        return self.__transaction_entry.destination_address

    @property
    def amount(self) -> float:
        return self.__transaction_entry.amount
