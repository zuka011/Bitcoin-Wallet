from dataclasses import dataclass
from typing import Optional
from uuid import uuid4

from core.repository.repository import InMemoryUserRepository


class InvalidApiKeyException(Exception):
    pass


@dataclass
class Wallet:
    pass


class UserInteractor:
    def __init__(
        self, user_repository: Optional[InMemoryUserRepository] = None
    ) -> None:
        self.__user_repository = user_repository

    def create_user(self, _: str) -> str:
        api_key = str(uuid4())
        if self.__user_repository is not None:
            self.__user_repository.api_keys.add(api_key)

        return api_key

    def create_wallet(self, api_key: str) -> Wallet:
        if (
            self.__user_repository is None
            or api_key not in self.__user_repository.api_keys
        ):
            raise InvalidApiKeyException(f"{api_key} is not a valid API key.")

        return Wallet()
