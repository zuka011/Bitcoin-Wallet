from typing import Final

from core import Currency

INITIAL_BALANCE: Final[float] = 1.0
PRIMARY_CURRENCY: Final[Currency] = Currency.BTC
SAME_USER_FEE: Final[float] = 0.0
CROSS_USER_FEE: Final[float] = 1.5
SYSTEM_WALLET_ADDRESS: Final[str] = "SYSTEM"
ADMIN_API_KEY: Final[str] = "I-AM-ADMIN.ADMIN-SMASH!"


class SystemConfiguration:
    @staticmethod
    def get_initial_balance() -> float:
        """Returns the initial balance of wallets."""
        return INITIAL_BALANCE

    @staticmethod
    def get_primary_currency() -> Currency:
        """Returns the primary currency used by the system."""
        return PRIMARY_CURRENCY

    @staticmethod
    def get_same_user_transfer_fee_percentage() -> float:
        """Returns the transfer fee (in percentages), for same-user transfers."""
        return SAME_USER_FEE

    @staticmethod
    def get_cross_user_transfer_fee_percentage() -> float:
        """Returns the transfer fee (in percentages), for cross-user transfers."""
        return CROSS_USER_FEE

    @staticmethod
    def get_system_wallet_address() -> str:
        """Returns the address of the system wallet. This is where all transactions fees are
        deposited to."""
        return SYSTEM_WALLET_ADDRESS

    @staticmethod
    def get_admin_api_key() -> str:
        """Returns the current Admin API key for the system."""
        return ADMIN_API_KEY
