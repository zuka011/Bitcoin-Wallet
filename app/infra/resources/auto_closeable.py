from typing import Protocol


class AutoCloseable(Protocol):
    def close(self) -> None:
        """Closes this resource."""
