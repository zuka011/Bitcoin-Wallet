from dataclasses import dataclass, field
from typing import Optional, Protocol, List
from uuid import uuid4

from core.repositories import IUserRepository
from infra.repositories import InMemoryUserRepository


class InvalidApiKeyException(Exception):
    pass


class InvalidUsernameException(Exception):
    pass


class IUsernameValidation(Protocol):
    def is_valid(self, username: str) -> bool:
        pass

class LongUsernameValidation:
    def __init__(self, boundary_length: int):
        self.__boundary_length = boundary_length

    def is_valid(self, username: str) -> bool:
        return len(username) <= self.__boundary_length

class ShortUsernameValidation:
    def __init__(self, boundary_length: int):
        self.__boundary_length = boundary_length

    def is_valid(self, username: str) -> bool:
        return len(username) >= self.__boundary_length


@dataclass
class Wallet:
    pass


@dataclass
class UserInteractor:
    user_repository: IUserRepository = InMemoryUserRepository(),
    validations: List[IUsernameValidation] = field(default_factory=list)

    def __is_valid(self, username: str) -> bool:
        return all([validation.is_valid(username) for validation in self.validations])

    def create_user(self, username: str) -> str:
        if self.__is_valid(username):
            if self.user_repository.has_username(username=username):
                raise InvalidUsernameException("Username already exists")
            api_key = str(uuid4())
            self.user_repository.add_user(api_key=api_key, username=username)
            return api_key
        else:
            raise InvalidUsernameException("Username out of boundaries")

    def create_wallet(self, api_key: str) -> Wallet:
        if not self.user_repository.has_api_key(api_key):
            raise InvalidApiKeyException(f"{api_key} is not a valid API key.")

        return Wallet()
