from typing import Protocol

from core.currencies import Currency


class ICurrencyConverter(Protocol):
    def convert(self, amount: float, *, source: Currency, target: Currency) -> float:
        """Converts the specified amount of the source currency to the target."""
