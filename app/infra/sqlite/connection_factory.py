import sqlite3
from sqlite3 import Connection
from typing import Final, Optional, Protocol


class ISqliteConnectionFactory(Protocol):
    def get_connection(self) -> Connection:
        """Returns a connection to an SQLite database."""

    def close(self) -> None:
        """Closes the connection to the SQLite database, if one exists."""


class SqliteConnectionFactory:
    def __init__(self, *, db_file: str) -> None:
        self.__db_file = db_file

    def get_connection(self) -> Connection:
        """Returns a connection to an SQLite database."""
        return sqlite3.connect(self.__db_file)

    def close(self) -> None:
        """Closes the connection to the SQLite database, if one exists."""


class InMemoryConnectionFactory:
    IN_MEMORY: Final[str] = ":memory:"

    def __init__(self) -> None:
        self.__connection: Optional[Connection] = None

    def get_connection(self) -> Connection:
        """Returns a connection to an SQLite database."""
        if self.__connection is None:
            self.__connection = sqlite3.connect(InMemoryConnectionFactory.IN_MEMORY)

        return self.__connection

    def close(self) -> None:
        """Closes the connection to the SQLite database, if one exists."""
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None
