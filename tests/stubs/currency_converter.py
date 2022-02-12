from dataclasses import dataclass

from core import Currency


@dataclass
class StubCurrencyConverter:
    btc_to_usd: float = 1

    def convert(self, amount: float, *, source: Currency, target: Currency) -> float:
        """Converts the specified amount of the source currency to the target."""
        if source == Currency.BTC and target == Currency.USD:
            return amount * self.btc_to_usd
        else:
            return amount
