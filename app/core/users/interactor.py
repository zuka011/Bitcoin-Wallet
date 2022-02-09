from dataclasses import dataclass
from typing import Optional, Protocol
from uuid import uuid4

from core.repositories import IUserRepository
from infra.repositories import InMemoryUserRepository


class InvalidApiKeyException(Exception):
    pass


class InvalidUsernameException(Exception):
    pass


class ICurrencyConverter(Protocol):
    def to_usd(self, btc: float) -> float:
        pass


@dataclass
class StubCurrencyConverter:
    exchange_rate: float

    def to_usd(self, btc: float) -> float:
        return btc * self.exchange_rate


@dataclass
class Wallet:
    address: str
    balance_btc: float
    balance_usd: float


class UserInteractor:
    def __init__(
        self,
        *,
        min_length: int = 0,
        max_length: Optional[int] = None,
        user_repository: IUserRepository = InMemoryUserRepository(),
        initial_balance: float = 0,
        currency_converter: ICurrencyConverter = StubCurrencyConverter(1),
    ) -> None:
        self.__min_length = min_length
        self.__max_length = max_length
        self.__user_repository = user_repository
        self.__initial_balance = initial_balance
        self.__currency_converter = currency_converter

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
        if not self.__user_repository.has_api_key(api_key):
            raise InvalidApiKeyException(f"{api_key} is not a valid API key.")
        address = str(uuid4())
        return Wallet(
            address=address,
            balance_btc=self.__initial_balance,
            balance_usd=self.__currency_converter.to_usd(self.__initial_balance),
        )
