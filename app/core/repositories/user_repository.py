from typing import Protocol


class IUserRepository(Protocol):
    def add_user(self, *, api_key: str, username: str) -> None:
        """Adds a user with the specified API key and username to this repository."""

    def has_api_key(self, api_key: str) -> bool:
        """Returns true if the specified API key exists in this repository."""

    def has_username(self, username: str) -> bool:
        """Returns true if the specified username exists in this repository."""
