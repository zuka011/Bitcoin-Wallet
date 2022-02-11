from typing import Iterable
from uuid import uuid4

from core.repositories import IUserRepository
from core.validators import IUsernameValidator


class UserInteractor:
    def __init__(
        self,
        *,
        user_repository: IUserRepository,
        username_validations: Iterable[IUsernameValidator] = (),
    ) -> None:
        self.__user_repository = user_repository
        self.__username_validations = username_validations

    def create_user(self, username: str) -> str:
        """Creates a user with the specified username and returns a newly generated API key."""
        self.__validate_username(username)

        api_key = str(uuid4())
        self.__user_repository.add_user(api_key=api_key, username=username)

        return api_key

    def __validate_username(self, username: str) -> None:
        """Validates the specified username against all username validators."""
        for validation in self.__username_validations:
            validation.is_valid(username)
