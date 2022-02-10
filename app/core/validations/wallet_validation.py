from collections import defaultdict
from typing import Dict, Protocol

from core.repositories import IUserRepository
from core.validations import InvalidApiKeyException, InvalidWalletRequestException


class IWalletValidator(Protocol):
    def validate_request(self, *, api_key: str) -> None:
        """Validates the specified request to create a new wallet."""


class WalletLimitValidator:
    def __init__(self, *, wallet_limit: int) -> None:
        self.__wallet_limit = wallet_limit
        self.__wallet_count: Dict[str, int] = defaultdict(lambda: 0)

    def validate_request(self, *, api_key: str) -> None:
        """Validates the specified request to create a new wallet.

        :raises InvalidWalletRequestException if the user has reached their wallet limit."""
        if (
            self.__wallet_limit is not None
            and self.__wallet_count[api_key] >= self.__wallet_limit
        ):
            raise InvalidWalletRequestException(
                f"You cannot create another wallet. You already have {self.__wallet_limit}."
            )

        self.__wallet_count[api_key] += 1


class WalletApiKeyValidator:
    def __init__(self, *, user_repository: IUserRepository) -> None:
        self.__user_repository = user_repository

    def validate_request(self, *, api_key: str) -> None:
        """Validates the specified request to create a new wallet.

        :raises InvalidApiKeyException if the users API key is not valid."""
        if not self.__user_repository.has_api_key(api_key):
            raise InvalidApiKeyException(f"{api_key} is not a valid API key.")
