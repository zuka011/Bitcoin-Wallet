from typing import Protocol


class ICurrencyConverter(Protocol):
    def to_usd(self, amount_btc: float) -> float:
        """Converts the specified amount of BTC to USD."""
