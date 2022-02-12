import string
from random import choice
from typing import Iterable, List
from uuid import uuid4

from core import Transaction, TransactionEntry


def random_string(length: int = 20) -> str:
    """Creates a random string of the specified length."""
    return "".join([choice(string.ascii_letters) for _ in range(length)])


def random_api_key() -> str:
    """Returns a random API key as a string."""
    return str(uuid4())


def sort_transactions(transactions: Iterable[Transaction]) -> List[Transaction]:
    """Returns a sorted list of all transactions in the specified iterable. The transactions
    are sorted by their timestamp in ascending order."""
    return sorted(transactions, key=lambda transaction: transaction.timestamp)


def sort_transaction_entries(
    transactions: Iterable[TransactionEntry],
) -> List[TransactionEntry]:
    """Returns a sorted list of all transactions in the specified iterable. The transactions
    are sorted by their timestamp in ascending order."""
    return sorted(transactions, key=lambda transaction: transaction.timestamp)
