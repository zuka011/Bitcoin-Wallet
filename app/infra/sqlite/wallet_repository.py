from core import WalletEntry
from infra.sqlite.sqlite import SqliteRepository


class SqliteWalletRepository(SqliteRepository):
    def add_wallet(self, wallet: WalletEntry, *, api_key: str) -> None:
        """Adds a wallet to this repository for the user with the specified API key."""
        self.update(
            "INSERT INTO wallets (address, balance, currency, api_key) "
            "VALUES (:address, :balance, :currency, :api_key)",
            parameters={
                "address": wallet.address,
                "balance": wallet.balance,
                "currency": wallet.currency,
                "api_key": api_key,
            },
        )

    def has_wallet(self, *, wallet_address: str) -> bool:
        """Returns true if a wallet with the specified address exists."""
        result = self.query(
            "SELECT COUNT(*) FROM wallets WHERE address=:address",
            parameters={"address": wallet_address},
        )
        return int(result.fetchone()[0]) > 0

    def get_wallet(self, *, wallet_address: str) -> WalletEntry:
        """Returns the wallet corresponding with the specified address."""
        assert self.has_wallet(
            wallet_address=wallet_address
        ), f"A wallet with the address {wallet_address} does not exist."

        address, balance, currency = self.query(
            "SELECT address, balance, currency FROM wallets WHERE address=:address",
            parameters={"address": wallet_address},
        ).fetchone()
        return WalletEntry(address=address, balance=balance, currency=currency)

    def update_wallet(self, wallet: WalletEntry, *, wallet_address: str) -> None:
        """Updates the wallet with the specified address."""
        assert self.has_wallet(
            wallet_address=wallet_address
        ), f"A wallet with the address {wallet_address} does not exist."
        assert (
            wallet_address == wallet.address
        ), "The specified wallet address differs from the one in the entry."

        self.update(
            "UPDATE wallets SET balance=:balance, currency=:currency "
            "WHERE address=:address",
            parameters={
                "address": wallet_address,
                "balance": wallet.balance,
                "currency": wallet.currency,
            },
        )

    def get_wallet_count(self, *, api_key: str) -> int:
        """Returns the number of wallets belonging to the user with the specified API key."""
        result = self.query(
            "SELECT COUNT(*) FROM wallets WHERE api_key=:api_key",
            parameters={"api_key": api_key},
        )
        return int(result.fetchone()[0])

    def is_wallet_owner(self, *, wallet_address: str, api_key: str) -> bool:
        """Returns true if wallet belongs to user with the specified API key."""
        assert self.has_wallet(
            wallet_address=wallet_address
        ), f"A wallet with the address {wallet_address} does not exist."

        return self.get_wallet_owner(wallet_address=wallet_address) == api_key

    def get_wallet_owner(self, *, wallet_address: str) -> str:
        """Returns the API key of the owner of the specified wallet."""
        assert self.has_wallet(
            wallet_address=wallet_address
        ), f"A wallet with the address {wallet_address} does not exist."

        result = self.query(
            "SELECT api_key FROM wallets WHERE address=:address",
            parameters={"address": wallet_address},
        ).fetchone()
        return str(result[0])
