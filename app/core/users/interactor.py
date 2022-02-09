from dataclasses import dataclass
from typing import Optional, Set
from uuid import uuid4

from core.users.repository import InMemoryUserRepository, InvalidUsernameException


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
        user_repository: Optional[InMemoryUserRepository] = None,
    ) -> None:
        self.__min_length = min_length
        self.__max_length = max_length
        self.__api_keys: Set[str] = set()
        self.__user_repository = user_repository

    def create_user(self, user_name: str) -> str:
        if len(user_name) < self.__min_length:
            raise InvalidUsernameException("Username is too short")
        if self.__max_length is not None and len(user_name) > self.__max_length:
            raise InvalidUsernameException("Username is too long")
        api_key = str(uuid4())
        self.__api_keys.add(api_key)

        if self.__user_repository is not None:
            self.__user_repository.api_keys.add(api_key)
            self.__user_repository.add_username(user_name)
        return api_key

    def create_wallet(self, api_key: str) -> Wallet:
        if api_key not in self.__api_keys and (
            self.__user_repository is None
            or api_key not in self.__user_repository.api_keys
        ):
            raise InvalidApiKeyException(f"{api_key} is not a valid API key.")

        return Wallet()
