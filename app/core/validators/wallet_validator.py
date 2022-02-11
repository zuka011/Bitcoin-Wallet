from typing import Protocol

from core.repositories import IUserRepository, IWalletRepository
from core.validators import InvalidApiKeyException, InvalidWalletRequestException


class IWalletValidator(Protocol):
    def validate_request(self, *, api_key: str) -> None:
        """Validates the specified request to create a new wallet."""


class WalletLimitValidator:
    def __init__(
        self, *, wallet_limit: int, wallet_repository: IWalletRepository
    ) -> None:
        self.__wallet_limit = wallet_limit
        self.__wallet_repository = wallet_repository

    def validate_request(self, *, api_key: str) -> None:
        """Validates the specified request to create a new wallet.

        :raises InvalidWalletRequestException if the user has reached their wallet limit."""
        if (
            self.__wallet_limit is not None
            and self.__wallet_repository.get_wallet_count(api_key=api_key)
            >= self.__wallet_limit
        ):
            raise InvalidWalletRequestException(
                f"You cannot create another wallet. You already have {self.__wallet_limit}."
            )


class WalletApiKeyValidator:
    def __init__(self, *, user_repository: IUserRepository) -> None:
        self.__user_repository = user_repository

    def validate_request(self, *, api_key: str) -> None:
        """Validates the specified request to create a new wallet.

        :raises InvalidApiKeyException if the users API key is not valid."""
        if not self.__user_repository.has_api_key(api_key):
            raise InvalidApiKeyException(f"{api_key} is not a valid API key.")
