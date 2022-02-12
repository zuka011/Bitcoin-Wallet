from dataclasses import dataclass

from core import Currency


@dataclass
class StubSystemConfiguration:
    initial_balance: float = 0
    primary_currency: Currency = Currency.BTC
    same_user_transfer_fee: float = 0
    cross_user_transfer_fee: float = 0

    def get_initial_balance(self) -> float:
        """Returns the initial balance of wallets."""
        return self.initial_balance

    def get_primary_currency(self) -> Currency:
        """Returns the primary currency used by the system."""
        return self.primary_currency

    def get_same_user_transfer_fee_percentage(self) -> float:
        """Returns the transfer fee (in percentages), for same-user transfers."""
        return self.same_user_transfer_fee

    def get_cross_user_transfer_fee_percentage(self) -> float:
        """Returns the transfer fee (in percentages), for cross-user transfers."""
        return self.cross_user_transfer_fee
