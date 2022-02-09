from dataclasses import dataclass
from typing import Protocol


@dataclass
class IUserRepository(Protocol):
    pass
