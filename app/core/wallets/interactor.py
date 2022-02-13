from typing import Iterable
from uuid import uuid4

from core.configurations import ISystemConfiguration
from core.converters.currency_converter import ICurrencyConverter
from core.repositories import IUserRepository, IWalletRepository, WalletEntry
from core.validators import InvalidApiKeyException, IWalletValidator
from core.wallets.wallet import Wallet


class WalletInteractor:
    def __init__(
        self,
        *,
        user_repository: IUserRepository,
        wallet_repository: IWalletRepository,
        currency_converter: ICurrencyConverter,
        system_configuration: ISystemConfiguration,
        wallet_validators: Iterable[IWalletValidator] = (),
    ) -> None:
        self.__user_repository = user_repository
        self.__wallet_repository = wallet_repository
        self.__system_configuration = system_configuration
        self.__currency_converter = currency_converter
        self.__wallet_validators = wallet_validators

    def create_wallet(self, api_key: str) -> Wallet:
        """Creates a wallet for the user with the specified API key and returns it."""
        for validator in self.__wallet_validators:
            validator.validate_request(api_key=api_key)

        wallet_entry = WalletEntry(
            address=str(uuid4()),
            balance=self.__system_configuration.get_initial_balance(),
            currency=self.__system_configuration.get_primary_currency(),
        )

        self.__wallet_repository.add_wallet(wallet_entry, api_key=api_key)
        return Wallet(
            wallet_entry=wallet_entry, currency_converter=self.__currency_converter
        )

    def get_wallet(self, *, address: str, api_key: str) -> Wallet:
        """Returns the wallet corresponding to the specified unique address.

        :raises InvalidApiKeyException if the wallet does not belong to the API key."""
        if not self.__wallet_repository.has_wallet(
            wallet_address=address
        ) or not self.__wallet_repository.is_wallet_owner(
            wallet_address=address, api_key=api_key
        ):
            raise InvalidApiKeyException("The address or API key is invalid.")

        return Wallet(
            wallet_entry=self.__wallet_repository.get_wallet(wallet_address=address),
            currency_converter=self.__currency_converter,
        )
