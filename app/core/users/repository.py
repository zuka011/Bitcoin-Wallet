from dataclasses import dataclass, field
from typing import List, Set

MAX_LENGTH = 10


@dataclass
class InMemoryUserRepository:
    usernames: List[str] = field(default_factory=list, init=False)
    api_keys: Set[str] = field(init=False, default_factory=set)

    def add_username(self, username: str) -> None:
        if username in self.usernames:
            raise InvalidUsernameException("Duplicate usernames")
        self.usernames.append(username)


class InvalidUsernameException(Exception):
    pass
