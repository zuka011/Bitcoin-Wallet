from typing import Protocol


class ISystemConfiguration(Protocol):
    def get_initial_balance_btc(self) -> float:
        """Returns the initial balance of wallets in BTC."""

    def get_transfer_fee_percentage(self) -> float:
        """Returns the transfer fee (in percentages), for cross-user transfers."""
