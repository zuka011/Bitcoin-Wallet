from dataclasses import dataclass


@dataclass
class StubSystemConfiguration:
    initial_balance: float = 0
    same_user_transfer_fee: float = 0
    cross_user_transfer_fee: float = 0

    def get_initial_balance_btc(self) -> float:
        """Returns the initial balance of wallets in BTC."""
        return self.initial_balance

    def get_same_user_transfer_fee_percentage(self) -> float:
        """Returns the transfer fee (in percentages), for same-user transfers."""
        return self.same_user_transfer_fee

    def get_cross_user_transfer_fee_percentage(self) -> float:
        """Returns the transfer fee (in percentages), for cross-user transfers."""
        return self.cross_user_transfer_fee
