from typing import Set


class InMemoryUserRepository:
    def __init__(self) -> None:
        self.__api_keys: Set[str] = set()
        self.__usernames: Set[str] = set()

    def add_user(self, *, api_key: str, username: str) -> None:
        self.__api_keys.add(api_key)
        self.__usernames.add(username)

    def has_api_key(self, api_key: str) -> bool:
        return api_key in self.__api_keys

    def has_username(self, username: str) -> bool:
        return username in self.__usernames
