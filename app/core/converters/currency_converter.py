from typing import Protocol


class ICurrencyConverter(Protocol):
    def to_usd(self, btc: float) -> float:
        pass
