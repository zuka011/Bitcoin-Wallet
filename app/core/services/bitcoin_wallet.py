from typing import Iterable

from core.statistics import StatisticsInteractor
from core.transactions import Transaction, TransactionInteractor
from core.users import UserInteractor
from core.wallets import Wallet, WalletInteractor


class BitcoinWalletService:
    def __init__(
        self,
        *,
        user_interactor: UserInteractor,
        wallet_interactor: WalletInteractor,
        transaction_interactor: TransactionInteractor,
        statistics_interactor: StatisticsInteractor,
    ) -> None:
        self.__user_interactor = user_interactor
        self.__wallet_interactor = wallet_interactor
        self.__transaction_interactor = transaction_interactor
        self.__statistics_interactor = statistics_interactor

    def create_user(self, username: str) -> str:
        """Creates a user with the specified username and returns a newly generated API key."""
        return self.__user_interactor.create_user(username)

    def create_wallet(self, api_key: str) -> Wallet:
        """Creates a wallet for the user with the specified API key and returns it."""
        return self.__wallet_interactor.create_wallet(api_key)

    def get_wallet(self, *, address: str, api_key: str) -> Wallet:
        """Returns the wallet corresponding to the specified unique address."""
        return self.__wallet_interactor.get_wallet(address=address, api_key=api_key)

    def transfer(
        self,
        *,
        api_key: str,
        source_address: str,
        destination_address: str,
        amount: float,
    ) -> None:
        """Transfers the specified amount from the source to the destination wallet. The API key of the owner
        of the source wallet is required for a successful transaction.

        :raises InvalidApiKeyException if the API key is not that of the owner of the source wallet."""
        self.__transaction_interactor.transfer(
            api_key=api_key,
            source_address=source_address,
            destination_address=destination_address,
            amount=amount,
        )

    def get_transactions(
        self, *, wallet_address: str, api_key: str
    ) -> Iterable[Transaction]:
        """Returns all transactions associated with the specified wallet address.

        :raises InvalidApiKeyException if the API key is not that of the owner of the wallet."""
        return self.__transaction_interactor.get_transactions(
            wallet_address=wallet_address, api_key=api_key
        )

    def get_user_transactions(self, *, api_key: str) -> Iterable[Transaction]:
        """Returns all transactions associated with the user with the specified API key."""
        return self.__transaction_interactor.get_user_transactions(api_key=api_key)

    def get_total_transactions(self, *, api_key: str) -> int:
        """Returns the total number of performed transactions on the platform."""
        return self.__statistics_interactor.get_total_transactions(api_key=api_key)

    def get_platform_profit(self, *, api_key: str) -> float:
        """Returns the total profit received by the system."""
        return self.__statistics_interactor.get_platform_profit(api_key=api_key)
