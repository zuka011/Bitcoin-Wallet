from typing import Optional
from uuid import uuid4

from core.repositories import IUserRepository
from core.validations import InvalidUsernameException


class UserInteractor:
    def __init__(
        self,
        *,
        user_repository: IUserRepository,
        min_length: int = 0,
        max_length: Optional[int] = None,
    ) -> None:
        self.__min_length = min_length
        self.__max_length = max_length
        self.__user_repository = user_repository

    def create_user(self, username: str) -> str:
        if len(username) < self.__min_length:
            raise InvalidUsernameException("Username is too short")

        if self.__max_length is not None and len(username) > self.__max_length:
            raise InvalidUsernameException("Username is too long")

        if self.__user_repository.has_username(username=username):
            raise InvalidUsernameException("Username already exists")

        api_key = str(uuid4())
        self.__user_repository.add_user(api_key=api_key, username=username)

        return api_key
