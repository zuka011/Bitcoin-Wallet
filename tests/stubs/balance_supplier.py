from dataclasses import dataclass


@dataclass
class StubBalanceSupplier:
    initial_balance: float = 0

    def get_initial_balance_btc(self) -> float:
        """Returns the initial balance of wallets in BTC."""
        return self.initial_balance
