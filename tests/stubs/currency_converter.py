from dataclasses import dataclass


@dataclass
class StubCurrencyConverter:
    exchange_rate: float = 1

    def to_usd(self, btc: float) -> float:
        return btc * self.exchange_rate
