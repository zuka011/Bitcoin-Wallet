from infra.sqlite.sqlite import SqliteRepository


class SqliteUserRepository(SqliteRepository):
    def add_user(self, *, api_key: str, username: str) -> None:
        """Adds a user with the specified API key and username to this repository."""
        self.update(
            "INSERT INTO users(api_key, username) VALUES (:api_key, :username)",
            parameters={"api_key": api_key, "username": username},
        )

    def has_api_key(self, api_key: str) -> bool:
        """Returns true if the specified API key exists in this repository."""
        result = self.query(
            "SELECT COUNT(*) FROM users WHERE api_key=:api_key",
            parameters={"api_key": api_key},
        )
        return float(result.fetchone()[0]) > 0

    def has_username(self, username: str) -> bool:
        """Returns true if the specified username exists in this repository."""
        result = self.query(
            "SELECT COUNT(*) FROM users WHERE username=:username",
            parameters={"username": username},
        )
        return float(result.fetchone()[0]) > 0
