from typing import Final

from core.configurations import ISystemConfiguration
from core.converters import ICurrencyConverter
from core.repositories import IWalletRepository, Wallet
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
        amount_btc: float,
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

        self.__withdraw_amount(wallet_address=source_address, amount_btc=amount_btc)
        self.__deposit_amount(
            wallet_address=destination_address,
            amount_btc=amount_btc,
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

    def __withdraw_amount(self, wallet_address: str, *, amount_btc: float) -> None:
        """Withdraws the specified amount from the given wallet."""
        wallet = self.__get_wallet(wallet_address)
        updated_balance_btc = wallet.balance_btc - amount_btc

        self.__update_wallet_balance(
            wallet_address=wallet_address, balance_btc=updated_balance_btc
        )

    def __deposit_amount(
        self, wallet_address: str, *, amount_btc: float, transfer_fee: float
    ) -> None:
        """Deposits the specified amount (after deducting transfer fee) to the given wallet."""
        wallet = self.__get_wallet(wallet_address)
        updated_balance_btc = wallet.balance_btc + deduct_percentage(
            amount_btc, transfer_fee
        )

        self.__update_wallet_balance(
            wallet_address=wallet_address, balance_btc=updated_balance_btc
        )

    def __get_wallet(self, wallet_address: str) -> Wallet:
        """Returns the wallet with the specified address."""
        return self.__wallet_repository.get_wallet(wallet_address=wallet_address)

    def __update_wallet_balance(
        self, wallet_address: str, *, balance_btc: float
    ) -> None:
        """Updates the balance of the specified wallet."""
        self.__wallet_repository.update_wallet(
            Wallet(
                address=wallet_address,
                balance_btc=balance_btc,
                balance_usd=self.__currency_converter.to_usd(balance_btc),
            ),
            wallet_address=wallet_address,
        )
