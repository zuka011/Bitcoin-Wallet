from typing import Protocol


class IUserRepository(Protocol):
    def add_user(self, *, api_key: str, username: str) -> None:
        pass

    def has_api_key(self, api_key: str) -> bool:
        pass

    def has_username(self, username: str) -> bool:
        pass
