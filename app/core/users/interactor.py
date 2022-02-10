from dataclasses import dataclass
from typing import Iterable, Optional
from uuid import uuid4

from core.converters.currency_converter import ICurrencyConverter
from core.repositories import IUserRepository
from core.validations import InvalidUsernameException, IWalletValidator


@dataclass(frozen=True)
class Wallet:
    address: str
    balance_btc: float
    balance_usd: float


class UserInteractor:
    def __init__(
        self,
        *,
        user_repository: IUserRepository,
        currency_converter: ICurrencyConverter,
        min_length: int = 0,
        max_length: Optional[int] = None,
        initial_balance: float = 0,
        wallet_validators: Iterable[IWalletValidator] = (),
    ) -> None:
        self.__min_length = min_length
        self.__max_length = max_length
        self.__user_repository = user_repository
        self.__initial_balance = initial_balance
        self.__currency_converter = currency_converter
        self.__wallet_validators = wallet_validators

    def create_user(self, username: str) -> str:
        if len(username) < self.__min_length:
            raise InvalidUsernameException("Username is too short")

        if self.__max_length is not None and len(username) > self.__max_length:
            raise InvalidUsernameException("Username is too long")

        if self.__user_repository.has_username(username=username):
            raise InvalidUsernameException("Username already exists")

        api_key = str(uuid4())
        self.__user_repository.add_user(api_key=api_key, username=username)

        return api_key

    def create_wallet(self, api_key: str) -> Wallet:
        for validator in self.__wallet_validators:
            validator.validate_request(api_key=api_key)

        return Wallet(
            address=str(uuid4()),
            balance_btc=self.__initial_balance,
            balance_usd=self.__currency_converter.to_usd(self.__initial_balance),
        )
