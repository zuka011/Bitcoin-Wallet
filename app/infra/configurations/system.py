from typing import Final

INITIAL_BALANCE: Final[float] = 1.0
SAME_USER_FEE: Final[float] = 0.0
CROSS_USER_FEE: Final[float] = 1.5


class SystemConfiguration:
    @staticmethod
    def get_initial_balance_btc() -> float:
        """Returns the initial balance of wallets in BTC."""
        return INITIAL_BALANCE

    @staticmethod
    def get_same_user_transfer_fee_percentage() -> float:
        """Returns the transfer fee (in percentages), for same-user transfers."""
        return SAME_USER_FEE

    @staticmethod
    def get_cross_user_transfer_fee_percentage() -> float:
        """Returns the transfer fee (in percentages), for cross-user transfers."""
        return CROSS_USER_FEE
