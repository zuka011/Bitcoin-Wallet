from datetime import datetime
from typing import Final, Iterable
from uuid import uuid4

from core.configurations import ISystemConfiguration
from core.converters import ICurrencyConverter
from core.currencies import Currency
from core.repositories import (
    ITransactionRepository,
    IWalletRepository,
    TransactionEntry,
    WalletEntry,
)
from core.transactions.transaction import Transaction
from core.validators import InvalidApiKeyException

HUNDRED_PERCENT: Final[int] = 100


def deduct_percentage(initial_value: float, percentage: float) -> float:
    """Deducts the specified percentage from the given value and returns the result."""
    return initial_value * (HUNDRED_PERCENT - percentage) / HUNDRED_PERCENT


class TransactionInteractor:
    def __init__(
        self,
        *,
        wallet_repository: IWalletRepository,
        transaction_repository: ITransactionRepository,
        currency_converter: ICurrencyConverter,
        system_configuration: ISystemConfiguration,
    ) -> None:
        self.__wallet_repository = wallet_repository
        self.__transaction_repository = transaction_repository
        self.__currency_converter = currency_converter
        self.__system_configuration = system_configuration

    def transfer(
        self,
        *,
        api_key: str,
        source_address: str,
        destination_address: str,
        amount: float,
    ) -> None:
        """Transfers the specified amount from the source to the destination wallet. The API key of the owner
        of the source wallet is required for a successful transaction.

        :raises InvalidApiKeyException if the API key is not that of the owner of the source wallet."""
        self.__validate_owner(wallet_address=source_address, api_key=api_key)

        withdraw_amount = self.__withdraw_amount(
            wallet_address=source_address, amount=amount
        )
        deposit_amount = self.__deposit_amount(
            wallet_address=destination_address,
            amount=amount,
            transfer_fee=self.__get_transfer_fee(
                destination_address=destination_address, api_key=api_key
            ),
        )

        self.__store_transactions(
            source_address=source_address,
            destination_address=destination_address,
            withdraw_amount=withdraw_amount,
            deposit_amount=deposit_amount,
        )

    def get_transactions(
        self, *, wallet_address: str, api_key: str
    ) -> Iterable[Transaction]:
        """Returns all transactions associated with the specified wallet address.

        :raises InvalidApiKeyException if the API key is not that of the owner of the wallet."""
        self.__validate_owner(wallet_address=wallet_address, api_key=api_key)

        return (
            Transaction(transaction_entry=transaction)
            for transaction in self.__transaction_repository.get_transactions(
                wallet_address=wallet_address
            )
        )

    def get_user_transactions(self, *, api_key: str) -> Iterable[Transaction]:
        """Returns all transactions associated with the user with the specified API key."""
        return (
            Transaction(transaction_entry=transaction)
            for transaction in self.__transaction_repository.get_user_transactions(
                api_key=api_key
            )
        )

    def __validate_owner(self, *, wallet_address: str, api_key: str) -> None:
        """Validates if the given wallet belongs to the user with the specified API key."""
        if not self.__wallet_repository.is_wallet_owner(
            wallet_address=wallet_address, api_key=api_key
        ):
            raise InvalidApiKeyException(
                "The specified source wallet or API key doesn't exist."
            )

    def __get_transfer_fee(self, *, destination_address: str, api_key: str) -> float:
        """Returns the transfer fee for transferring to the specified wallet address."""
        if self.__wallet_repository.is_wallet_owner(
            wallet_address=destination_address, api_key=api_key
        ):
            return self.__system_configuration.get_same_user_transfer_fee_percentage()
        else:
            return self.__system_configuration.get_cross_user_transfer_fee_percentage()

    def __withdraw_amount(self, wallet_address: str, *, amount: float) -> float:
        """Withdraws the specified amount from the given wallet.

        :returns The amount withdrawn from the specified wallet."""
        wallet = self.__get_wallet(wallet_address)
        withdrawal_amount = amount
        updated_balance = wallet.balance - withdrawal_amount

        self.__update_wallet_balance(
            wallet_address=wallet_address,
            balance=updated_balance,
            currency=wallet.currency,
        )

        return withdrawal_amount

    def __deposit_amount(
        self, wallet_address: str, *, amount: float, transfer_fee: float
    ) -> float:
        """Deposits the specified amount (after deducting transfer fee) to the given wallet.

        :returns The amount deposited to the specified wallet."""
        wallet = self.__get_wallet(wallet_address)
        deposit_amount = deduct_percentage(amount, transfer_fee)
        updated_balance = wallet.balance + deposit_amount

        self.__update_wallet_balance(
            wallet_address=wallet_address,
            balance=updated_balance,
            currency=wallet.currency,
        )

        return deposit_amount

    def __get_wallet(self, wallet_address: str) -> WalletEntry:
        """Returns the wallet with the specified address."""
        return self.__wallet_repository.get_wallet(wallet_address=wallet_address)

    def __update_wallet_balance(
        self, wallet_address: str, *, balance: float, currency: Currency
    ) -> None:
        """Updates the balance of the specified wallet."""
        self.__wallet_repository.update_wallet(
            WalletEntry(
                address=wallet_address,
                balance=balance,
                currency=currency,
            ),
            wallet_address=wallet_address,
        )

    def __store_transactions(
        self,
        *,
        source_address: str,
        destination_address: str,
        withdraw_amount: float,
        deposit_amount: float,
    ) -> None:
        """Stores a transaction describing a withdrawal from the source wallet."""
        transaction = TransactionEntry(
            id=str(uuid4()),
            source_address=source_address,
            destination_address=destination_address,
            amount=deposit_amount,
            timestamp=datetime.now(),
        )

        # Link main transaction with first wallet.
        self.__transaction_repository.add_transaction(
            transaction, wallet_address=source_address
        )

        # Link main transaction with second wallet.
        self.__transaction_repository.add_transaction(
            transaction, wallet_address=destination_address
        )

        if withdraw_amount != deposit_amount:
            # Link system fee transaction (deposit to system wallet) with first wallet.
            self.__transaction_repository.add_transaction(
                TransactionEntry(
                    id=str(uuid4()),
                    source_address=source_address,
                    destination_address=self.__system_configuration.get_system_wallet_address(),
                    amount=(withdraw_amount - deposit_amount),
                    timestamp=datetime.now(),
                ),
                wallet_address=source_address,
            )
