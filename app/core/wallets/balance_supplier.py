from typing import Protocol


class IBalanceSupplier(Protocol):
    def get_initial_balance_btc(self) -> float:
        """Returns the initial balance of wallets in BTC."""
