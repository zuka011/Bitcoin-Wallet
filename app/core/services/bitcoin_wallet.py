from core.repositories import Wallet
from core.users import UserInteractor
from core.wallets import WalletInteractor


class BitcoinWalletService:
    def __init__(
        self, *, user_interactor: UserInteractor, wallet_interactor: WalletInteractor
    ) -> None:
        self.__user_interactor = user_interactor
        self.__wallet_interactor = wallet_interactor

    def create_user(self, username: str) -> str:
        """Creates a user with the specified username and returns a newly generated API key."""
        return self.__user_interactor.create_user(username)

    def create_wallet(self, api_key: str) -> Wallet:
        """Creates a wallet for the user with the specified API key and returns it."""
        return self.__wallet_interactor.create_wallet(api_key)
