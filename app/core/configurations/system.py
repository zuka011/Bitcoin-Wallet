from typing import Protocol

from core.currencies import Currency


class ISystemConfiguration(Protocol):
    def get_initial_balance(self) -> float:
        """Returns the initial balance of wallets."""

    def get_primary_currency(self) -> Currency:
        """Returns the primary currency used by the system."""

    def get_same_user_transfer_fee_percentage(self) -> float:
        """Returns the transfer fee (in percentages), for same-user transfers."""

    def get_cross_user_transfer_fee_percentage(self) -> float:
        """Returns the transfer fee (in percentages), for cross-user transfers."""
