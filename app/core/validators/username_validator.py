from typing import Protocol

from core.repositories import IUserRepository
from core.validators.exception import InvalidUsernameException


class IUsernameValidator(Protocol):
    def is_valid(self, username: str) -> None:
        """Validates the specified username.

        :raises InvalidUsernameException if the username is invalid."""


class LongUsernameValidator:
    def __init__(self, *, max_length: int) -> None:
        self.__max_length = max_length

    def is_valid(self, username: str) -> None:
        """Validates the specified username.

        :raises InvalidUsernameException if the username is too long."""
        if len(username) > self.__max_length:
            raise InvalidUsernameException(
                f"A username must not be longer than {self.__max_length} characters."
            )


class ShortUsernameValidator:
    def __init__(self, *, min_length: int) -> None:
        self.__min_length = min_length

    def is_valid(self, username: str) -> None:
        """Validates the specified username.

        :raises InvalidUsernameException if the username is too short."""
        if len(username) < self.__min_length:
            raise InvalidUsernameException(
                f"A username must not be shorter than {self.__min_length} characters."
            )


class DuplicateUsernameValidator:
    def __init__(self, *, user_repository: IUserRepository) -> None:
        self.__user_repository = user_repository

    def is_valid(self, username: str) -> None:
        """Validates the specified username.

        :raises InvalidUsernameException if the username already exists."""
        if self.__user_repository.has_username(username=username):
            raise InvalidUsernameException(f"The username '{username}' already exists.")
