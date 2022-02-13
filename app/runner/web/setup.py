import os
from typing import Callable, Final, Iterable, Optional, TypeVar

from fastapi import FastAPI

from core import (
    BitcoinWalletService,
    DuplicateUsernameValidator,
    ICurrencyConverter,
    InvalidApiKeyException,
    InvalidTransactionRequestException,
    InvalidUsernameException,
    InvalidWalletRequestException,
    IStatisticsRepository,
    ISystemConfiguration,
    ITransactionRepository,
    IUsernameValidator,
    IUserRepository,
    IWalletRepository,
    IWalletValidator,
    LongUsernameValidator,
    ShortUsernameValidator,
    StatisticsInteractor,
    TransactionInteractor,
    UserInteractor,
    WalletApiKeyValidator,
    WalletInteractor,
    WalletLimitValidator,
)
from infra import (
    AutoCloseable,
    SqliteConnectionFactory,
    SqliteStatisticsRepository,
    SqliteTransactionRepository,
    SqliteUserRepository,
    SqliteWalletRepository,
    help_api,
    invalid_api_key_exception_handler,
    invalid_transaction_request_exception_handler,
    invalid_username_exception_handler,
    invalid_wallet_request_exception_handler,
    statistics_api,
    transaction_api,
    user_api,
    wallet_api,
)

USERS_SQL: Final[str] = "data_base/users.sql"
WALLETS_SQL: Final[str] = "data_base/wallets.sql"
TRANSACTIONS_SQL: Final[str] = "data_base/transactions.sql"
STATISTICS_SQL: Final[str] = "data_base/statistics.sql"
BITCOIN_WALLET_DB: Final[str] = "data_base/bitcoin_wallet.sqlite"

MIN_USERNAME_LENGTH: Final[int] = 8
MAX_USERNAME_LENGTH: Final[int] = 20

MAX_WALLET_COUNT: Final[int] = 3

T = TypeVar("T", bound=AutoCloseable)
S = TypeVar("S")


def with_shutdown_hook(function: Callable[[FastAPI], T]) -> Callable[[FastAPI], T]:
    """Adds a shutdown hook for the resource returned by the specified callable."""

    def wrapper(app: FastAPI) -> T:
        repository = function(app)

        @app.on_event("shutdown")
        def shutdown_hook() -> None:
            print(f"Shutting down resource. Class: {repository.__class__.__name__}")
            repository.close()

        return repository

    return wrapper


def with_db_file(function: Callable[[FastAPI], S]) -> Callable[[FastAPI], S]:
    """Will create a default DB file for SQLite if one doesn't exist."""

    def wrapper(app: FastAPI) -> S:
        if not os.path.isfile(BITCOIN_WALLET_DB):
            open(BITCOIN_WALLET_DB, "w").close()

        return function(app)

    return wrapper


@with_db_file
@with_shutdown_hook
def sqlite_user_repository(_app: FastAPI) -> SqliteUserRepository:
    """Returns a persistent SQLite user repository."""
    return SqliteUserRepository(
        connection_factory=SqliteConnectionFactory(db_file=BITCOIN_WALLET_DB),
        init_files=[USERS_SQL],
    )


@with_db_file
@with_shutdown_hook
def sqlite_wallet_repository(_app: FastAPI) -> SqliteWalletRepository:
    """Returns a persistent SQLite wallet repository."""
    return SqliteWalletRepository(
        connection_factory=SqliteConnectionFactory(db_file=BITCOIN_WALLET_DB),
        init_files=[USERS_SQL, WALLETS_SQL],
    )


@with_db_file
@with_shutdown_hook
def sqlite_transaction_repository(_app: FastAPI) -> SqliteTransactionRepository:
    """Returns a persistent SQLite transaction repository."""
    return SqliteTransactionRepository(
        connection_factory=SqliteConnectionFactory(db_file=BITCOIN_WALLET_DB),
        init_files=[USERS_SQL, WALLETS_SQL, TRANSACTIONS_SQL],
    )


@with_db_file
@with_shutdown_hook
def sqlite_statistics_repository(_app: FastAPI) -> SqliteStatisticsRepository:
    """Returns a persistent SQLite statistics repository."""
    return SqliteStatisticsRepository(
        connection_factory=SqliteConnectionFactory(db_file=BITCOIN_WALLET_DB),
        init_files=[USERS_SQL, WALLETS_SQL, TRANSACTIONS_SQL, STATISTICS_SQL],
    )


def default_username_validators(
    *,
    user_repository: IUserRepository,
) -> Iterable[IUsernameValidator]:
    """Returns the default username validators for the system."""
    return (
        DuplicateUsernameValidator(user_repository=user_repository),
        ShortUsernameValidator(min_length=MIN_USERNAME_LENGTH),
        LongUsernameValidator(max_length=MAX_USERNAME_LENGTH),
    )


def default_wallet_validators(
    *, user_repository: IUserRepository, wallet_repository: IWalletRepository
) -> Iterable[IWalletValidator]:
    """Returns the default wallet validators for the system."""
    return (
        WalletLimitValidator(
            wallet_limit=MAX_WALLET_COUNT, wallet_repository=wallet_repository
        ),
        WalletApiKeyValidator(user_repository=user_repository),
    )


def setup(
    *,
    user_repository: Optional[IUserRepository] = None,
    wallet_repository: Optional[IWalletRepository] = None,
    transaction_repository: Optional[ITransactionRepository] = None,
    statistics_repository: Optional[IStatisticsRepository] = None,
    currency_converter: ICurrencyConverter,
    system_configuration: ISystemConfiguration,
    username_validators: Optional[Iterable[IUsernameValidator]] = None,
    wallet_validators: Optional[Iterable[IWalletValidator]] = None,
) -> FastAPI:
    app = FastAPI()
    app.include_router(help_api)
    app.include_router(user_api)
    app.include_router(wallet_api)
    app.include_router(transaction_api)
    app.include_router(statistics_api)

    user_repository = user_repository or sqlite_user_repository(app)
    wallet_repository = wallet_repository or sqlite_wallet_repository(app)
    transaction_repository = transaction_repository or sqlite_transaction_repository(
        app
    )
    statistics_repository = statistics_repository or sqlite_statistics_repository(app)

    if username_validators is None:
        username_validators = default_username_validators(
            user_repository=user_repository
        )

    if wallet_validators is None:
        wallet_validators = default_wallet_validators(
            user_repository=user_repository, wallet_repository=wallet_repository
        )

    app.state.core = BitcoinWalletService(
        user_interactor=UserInteractor(
            user_repository=user_repository,
            username_validators=username_validators,
        ),
        wallet_interactor=WalletInteractor(
            user_repository=user_repository,
            wallet_repository=wallet_repository,
            currency_converter=currency_converter,
            system_configuration=system_configuration,
            wallet_validators=wallet_validators,
        ),
        transaction_interactor=TransactionInteractor(
            wallet_repository=wallet_repository,
            transaction_repository=transaction_repository,
            statistics_repository=statistics_repository,
            currency_converter=currency_converter,
            system_configuration=system_configuration,
        ),
        statistics_interactor=StatisticsInteractor(
            statistics_repository=statistics_repository,
            system_configuration=system_configuration,
        ),
    )

    app.exception_handler(InvalidUsernameException)(invalid_username_exception_handler)
    app.exception_handler(InvalidApiKeyException)(invalid_api_key_exception_handler)
    app.exception_handler(InvalidWalletRequestException)(
        invalid_wallet_request_exception_handler
    )
    app.exception_handler(InvalidTransactionRequestException)(
        invalid_transaction_request_exception_handler
    )

    return app
