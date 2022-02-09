from typing import Protocol


class IUserRepository(Protocol):
    def add_user(self, *, api_key: str) -> None:
        pass

    def has_api_key(self, api_key: str) -> bool:
        pass
