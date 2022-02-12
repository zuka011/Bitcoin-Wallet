from typing import Any

from core import Currency, ICurrencyConverter
from core.repositories import WalletEntry


class Wallet:
    def __init__(
        self, *, wallet_entry: WalletEntry, currency_converter: ICurrencyConverter
    ) -> None:
        self.__wallet_entry = wallet_entry
        self.__currency_converter = currency_converter

    def get_balance(self, *, currency: Currency) -> float:
        """Returns the balance of this wallet in the specified currency."""
        return self.__currency_converter.convert(
            self.__wallet_entry.balance,
            source=self.__wallet_entry.currency,
            target=currency,
        )

    @property
    def address(self) -> str:
        """Returns the unique address of this wallet."""
        return self.__wallet_entry.address

    @property
    def primary_currency(self) -> Currency:
        """Returns the primary currency of this wallet."""
        return self.__wallet_entry.currency

    def __eq__(self, other: Any) -> bool:
        assert isinstance(other, Wallet), f"Cannot compare a Wallet with {type(other)}."

        return self.__wallet_entry == other.__wallet_entry
