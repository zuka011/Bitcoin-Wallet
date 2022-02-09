from dataclasses import dataclass
from uuid import uuid4

from core.repositories import IUserRepository
from infra.repositories import InMemoryUserRepository


class InvalidApiKeyException(Exception):
    pass


@dataclass
class Wallet:
    pass


class UserInteractor:
    def __init__(
            self,
            *,
            min_length: int = 0,
            max_length: Optional[int] = None,
            user_repository: IUserRepository = InMemoryUserRepository()
    ) -> None:
        self.__min_length = min_length
        self.__max_length = max_length
        self.__user_repository = user_repository

    def create_user(self, _: str) -> str:
        if len(user_name) < self.__min_length:
            raise InvalidUsernameException("Username is too short")
        if self.__max_length is not None and len(user_name) > self.__max_length:
            raise InvalidUsernameException("Username is too long")

        api_key = str(uuid4())
        self.__user_repository.add_user(api_key=api_key)

        return api_key

    def create_wallet(self, api_key: str) -> Wallet:
        if not self.__user_repository.has_api_key(api_key):
            raise InvalidApiKeyException(f"{api_key} is not a valid API key.")

        return Wallet()
