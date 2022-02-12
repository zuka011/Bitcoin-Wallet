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

    def get_system_wallet_address(self) -> str:
        """Returns the address of the system wallet. This is where all transactions fees are
        deposited to."""

    def get_admin_api_key(self) -> str:
        """Returns the current Admin API key for the system."""
