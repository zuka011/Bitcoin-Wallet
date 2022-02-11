from core.users import UserInteractor


class BitcoinWalletService:
    def __init__(self, *, user_interactor: UserInteractor) -> None:
        self.__user_interactor = user_interactor

    def create_user(self, username: str) -> str:
        """Creates a user with the specified username and returns a newly generated API key."""
        return self.__user_interactor.create_user(username)
