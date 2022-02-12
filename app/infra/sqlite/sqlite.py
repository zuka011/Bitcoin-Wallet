from sqlite3 import Cursor
from typing import Any, Iterable, Sequence, TypeVar

from infra.sqlite.connection_factory import ISqliteConnectionFactory

T = TypeVar("T", bound="SqliteRepository")


class SqliteRepository:
    def __init__(
        self, *, connection_factory: ISqliteConnectionFactory, init_files: Sequence[str]
    ) -> None:
        """Creates an SQLite repository."""
        self.__connection_factory = connection_factory
        self.__initialize_data_base(init_files=init_files)

    def __enter__(self: T) -> T:
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        self.close()

    def update(self, sql: str, parameters: Iterable[Any] = ()) -> None:
        """Executes the specified SQL statement to update the data base."""
        with self.__connection_factory.get_connection() as connection:
            connection.execute(sql, parameters)
            connection.commit()

    def query(self, sql: str, parameters: Iterable[Any] = ()) -> Cursor:
        """Executes the specified SQL statement and returns the result."""
        with self.__connection_factory.get_connection() as connection:
            return connection.execute(sql, parameters)

    def __initialize_data_base(self, *, init_files: Sequence[str]) -> None:
        """Initializes the data base according to the specified initialization files."""
        with self.__connection_factory.get_connection() as connection:
            for init_file in init_files:
                sql_script: str

                with open(file=init_file, mode="r") as sql_file:
                    sql_script = sql_file.read()

                connection.executescript(sql_script)

            connection.commit()

    def close(self) -> None:
        """Closes the connection to the SQLite DB."""
        self.__connection_factory.close()
