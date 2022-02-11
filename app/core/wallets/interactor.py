from typing import Iterable
from uuid import uuid4

from core.converters.currency_converter import ICurrencyConverter
from core.repositories import IUserRepository, IWalletRepository, Wallet
from core.validations import IWalletValidator


class WalletInteractor:
    def __init__(
        self,
        *,
        user_repository: IUserRepository,
        wallet_repository: IWalletRepository,
        currency_converter: ICurrencyConverter,
        initial_balance: float = 0,
        wallet_validators: Iterable[IWalletValidator] = (),
    ) -> None:
        self.__user_repository = user_repository
        self.__wallet_repository = wallet_repository
        self.__initial_balance = initial_balance
        self.__currency_converter = currency_converter
        self.__wallet_validators = wallet_validators

    def create_wallet(self, api_key: str) -> Wallet:
        for validator in self.__wallet_validators:
            validator.validate_request(api_key=api_key)

        wallet = Wallet(
            address=str(uuid4()),
            balance_btc=self.__initial_balance,
            balance_usd=self.__currency_converter.to_usd(self.__initial_balance),
        )

        self.__wallet_repository.add_wallet(wallet, api_key=api_key)
        return wallet

    def get_wallet(self, *, address: str) -> Wallet:
        return self.__wallet_repository.get_wallet(wallet_address=address)
