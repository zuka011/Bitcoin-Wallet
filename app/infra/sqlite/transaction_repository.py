from datetime import datetime
from typing import Iterable

from core import TransactionEntry
from infra.sqlite.sqlite import SqliteRepository


class SqliteTransactionRepository(SqliteRepository):
    def add_transaction(
        self, transaction: TransactionEntry, *, wallet_address: str
    ) -> None:
        """Adds the transaction for the specified wallet to the this repository."""

        self.update(
            "INSERT INTO transactions ("
            "   associated_wallet, "
            "   associated_api_key, "
            "   id, "
            "   source_address, "
            "   destination_address, "
            "   amount, "
            "   timestamp"
            ") VALUES ("
            "   :associated_wallet, "
            "   :associated_api_key, "
            "   :id, "
            "   :source_address, "
            "   :destination_address,"
            "   :amount,"
            "   :timestamp"
            ")",
            parameters={
                "associated_wallet": wallet_address,
                "associated_api_key": self.__get_wallet_owner(wallet_address),
                "id": transaction.id,
                "source_address": transaction.source_address,
                "destination_address": transaction.destination_address,
                "amount": transaction.amount,
                "timestamp": transaction.timestamp,
            },
        )

    def get_transactions(self, *, wallet_address: str) -> Iterable[TransactionEntry]:
        """Returns all transactions associated with the specified wallet address."""
        result = self.query(
            "SELECT id, source_address, destination_address, amount, timestamp FROM transactions "
            "WHERE associated_wallet=:address",
            parameters={"address": wallet_address},
        )

        return (
            TransactionEntry(
                id=transaction_id,
                source_address=source_address,
                destination_address=destination_address,
                amount=amount,
                timestamp=datetime.fromisoformat(timestamp),
            )
            for transaction_id, source_address, destination_address, amount, timestamp in result
        )

    def get_user_transactions(self, *, api_key: str) -> Iterable[TransactionEntry]:
        """Returns all transactions associated with the user with the specified API key."""
        result = self.query(
            "SELECT id, source_address, destination_address, amount, timestamp FROM transactions "
            "WHERE associated_api_key=:api_key",
            parameters={"api_key": api_key},
        )

        return (
            TransactionEntry(
                id=transaction_id,
                source_address=source_address,
                destination_address=destination_address,
                amount=amount,
                timestamp=datetime.fromisoformat(timestamp),
            )
            for transaction_id, source_address, destination_address, amount, timestamp in result
        )

    def __get_wallet_owner(self, wallet_address: str) -> str:
        """Returns the API key of the owner of the specified wallet."""
        result = self.query(
            "SELECT api_key FROM wallets WHERE address=:address",
            parameters={"address": wallet_address},
        ).fetchone()
        return str(result[0])
