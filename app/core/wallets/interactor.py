from dataclasses import dataclass
from uuid import uuid4

from core import IUserRepository
from core.converters.currency_converter import ICurrencyConverter


class InvalidApiKeyException(Exception):
    pass


@dataclass(frozen=True)
class Wallet:
    address: str
    balance_btc: float
    balance_usd: float


class WalletInteractor:
    def __init__(
        self,
        *,
        user_repository: IUserRepository,
        currency_converter: ICurrencyConverter,
        initial_balance: float = 0,
    ) -> None:
        self.__user_repository = user_repository
        self.__initial_balance = initial_balance
        self.__currency_converter = currency_converter

    def create_wallet(self, api_key: str) -> Wallet:
        if not self.__user_repository.has_api_key(api_key):
            raise InvalidApiKeyException(f"{api_key} is not a valid API key.")

        return Wallet(
            address=str(uuid4()),
            balance_btc=self.__initial_balance,
            balance_usd=self.__currency_converter.to_usd(self.__initial_balance),
        )
