from typing import Final

from core.configurations import ISystemConfiguration
from core.converters import ICurrencyConverter
from core.currencies import Currency
from core.repositories import IWalletRepository, WalletEntry
from core.validators import InvalidApiKeyException

HUNDRED_PERCENT: Final[int] = 100


def deduct_percentage(initial_value: float, percentage: float) -> float:
    """Deducts the specified percentage from the given value and returns the result."""
    return initial_value * (HUNDRED_PERCENT - percentage) / HUNDRED_PERCENT


class TransactionInteractor:
    def __init__(
        self,
        *,
        wallet_repository: IWalletRepository,
        currency_converter: ICurrencyConverter,
        system_configuration: ISystemConfiguration,
    ) -> None:
        self.__wallet_repository = wallet_repository
        self.__currency_converter = currency_converter
        self.__system_configuration = system_configuration

    def transfer(
        self,
        api_key: str,
        source_address: str,
        destination_address: str,
        amount: float,
    ) -> None:
        """Transfers the specified amount from the source to the destination wallet. The API key of the owner
        of the source wallet is required for a successful transaction.

        :raises InvalidApiKeyException if the API key is not that of the owner of the source wallet."""
        if not self.__wallet_repository.is_wallet_owner(
            wallet_address=source_address, api_key=api_key
        ):
            raise InvalidApiKeyException(
                f"Cannot transfer funds from {source_address} with incorrect API key."
            )

        transfer_fee = self.__get_transfer_fee(
            source_address=source_address,
            destination_address=destination_address,
            api_key=api_key,
        )

        self.__withdraw_amount(wallet_address=source_address, amount=amount)
        self.__deposit_amount(
            wallet_address=destination_address,
            amount=amount,
            transfer_fee=transfer_fee,
        )

    def __get_transfer_fee(
        self, *, source_address: str, destination_address: str, api_key: str
    ) -> float:
        """Returns the transfer fee for transferring to the specified wallet address."""
        if self.__wallet_repository.is_wallet_owner(
            wallet_address=destination_address, api_key=api_key
        ):
            return self.__system_configuration.get_same_user_transfer_fee_percentage()
        else:
            return self.__system_configuration.get_cross_user_transfer_fee_percentage()

    def __withdraw_amount(self, wallet_address: str, *, amount: float) -> None:
        """Withdraws the specified amount from the given wallet."""
        wallet = self.__get_wallet(wallet_address)
        updated_balance = wallet.balance - amount

        self.__update_wallet_balance(
            wallet_address=wallet_address,
            balance=updated_balance,
            currency=wallet.currency,
        )

    def __deposit_amount(
        self, wallet_address: str, *, amount: float, transfer_fee: float
    ) -> None:
        """Deposits the specified amount (after deducting transfer fee) to the given wallet."""
        wallet = self.__get_wallet(wallet_address)
        updated_balance = wallet.balance + deduct_percentage(amount, transfer_fee)

        self.__update_wallet_balance(
            wallet_address=wallet_address,
            balance=updated_balance,
            currency=wallet.currency,
        )

    def __get_wallet(self, wallet_address: str) -> WalletEntry:
        """Returns the wallet with the specified address."""
        return self.__wallet_repository.get_wallet(wallet_address=wallet_address)

    def __update_wallet_balance(
        self, wallet_address: str, *, balance: float, currency: Currency
    ) -> None:
        """Updates the balance of the specified wallet."""
        self.__wallet_repository.update_wallet(
            WalletEntry(
                address=wallet_address,
                balance=balance,
                currency=currency,
            ),
            wallet_address=wallet_address,
        )
