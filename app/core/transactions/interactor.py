from typing import Final

from core.configurations import ISystemConfiguration
from core.converters import ICurrencyConverter
from core.repositories import IWalletRepository, Wallet
from core.validations import InvalidApiKeyException

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
        if not self.__wallet_repository.is_wallet_owner(
            wallet_address=source_address, api_key=api_key
        ):
            raise InvalidApiKeyException(
                f"Cannot transfer funds from {source_address} with incorrect API key."
            )

        if self.__wallet_repository.is_wallet_owner(
            wallet_address=destination_address, api_key=api_key
        ):
            transfer_fee = (
                self.__system_configuration.get_same_user_transfer_fee_percentage()
            )
        else:
            transfer_fee = (
                self.__system_configuration.get_cross_user_transfer_fee_percentage()
            )

        source_wallet = self.__wallet_repository.get_wallet(
            wallet_address=source_address
        )
        destination_wallet = self.__wallet_repository.get_wallet(
            wallet_address=destination_address
        )

        updated_source_balance_btc = source_wallet.balance_btc - amount_btc
        updated_destination_balance_btc = (
            destination_wallet.balance_btc + deduct_percentage(amount_btc, transfer_fee)
        )

        self.__wallet_repository.update_wallet(
            Wallet(
                address=source_address,
                balance_btc=updated_source_balance_btc,
                balance_usd=self.__currency_converter.to_usd(
                    updated_source_balance_btc
                ),
            ),
            wallet_address=source_address,
        )
        self.__wallet_repository.update_wallet(
            Wallet(
                address=destination_address,
                balance_btc=updated_destination_balance_btc,
                balance_usd=self.__currency_converter.to_usd(
                    updated_destination_balance_btc
                ),
            ),
            wallet_address=destination_address,
        )
