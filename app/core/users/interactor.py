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
            self, user_repository: IUserRepository = InMemoryUserRepository()
    ) -> None:
        self.__user_repository = user_repository

    def create_user(self, _: str) -> str:
        api_key = str(uuid4())
        self.__user_repository.add_user(api_key=api_key)

        return api_key

    def create_wallet(self, api_key: str) -> Wallet:
        if not self.__user_repository.has_api_key(api_key):
            raise InvalidApiKeyException(f"{api_key} is not a valid API key.")

        return Wallet()
