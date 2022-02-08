from dataclasses import dataclass, field
from typing import Set


@dataclass
class InMemoryUserRepository:
    api_keys: Set[str] = field(init=False, default_factory=set)
