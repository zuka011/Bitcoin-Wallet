from typing import Iterable

from core import (
    BitcoinWalletService,
    ICurrencyConverter,
    InvalidUsernameException,
    IStatisticsRepository,
    ISystemConfiguration,
    ITransactionRepository,
    IUsernameValidator,
    IUserRepository,
    IWalletRepository,
    StatisticsInteractor,
    TransactionInteractor,
    UserInteractor,
    WalletInteractor,
)
from fastapi import FastAPI
from infra import (
    help_api,
    invalid_username_exception_handler,
    statistics_api,
    transaction_api,
    user_api,
    wallet_api,
)


def setup(
    *,
    user_repository: IUserRepository,
    wallet_repository: IWalletRepository,
    transaction_repository: ITransactionRepository,
    statistics_repository: IStatisticsRepository,
    currency_converter: ICurrencyConverter,
    system_configuration: ISystemConfiguration,
    username_validators: Iterable[IUsernameValidator] = ()
) -> FastAPI:
    app = FastAPI()
    app.include_router(help_api)
    app.include_router(user_api)
    app.include_router(wallet_api)
    app.include_router(transaction_api)
    app.include_router(statistics_api)

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

    return app
