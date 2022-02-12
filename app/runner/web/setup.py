from core import (
    BitcoinWalletService,
    ICurrencyConverter,
    IStatisticsRepository,
    ISystemConfiguration,
    ITransactionRepository,
    IUserRepository,
    IWalletRepository,
    TransactionInteractor,
    UserInteractor,
    WalletInteractor,
)
from fastapi import FastAPI
from infra import help_api, transaction_api, user_api, wallet_api


def setup(
    *,
    user_repository: IUserRepository,
    wallet_repository: IWalletRepository,
    transaction_repository: ITransactionRepository,
    statistics_repository: IStatisticsRepository,
    currency_converter: ICurrencyConverter,
    system_configuration: ISystemConfiguration
) -> FastAPI:
    app = FastAPI()
    app.include_router(help_api)
    app.include_router(user_api)
    app.include_router(wallet_api)
    app.include_router(transaction_api)

    app.state.core = BitcoinWalletService(
        user_interactor=UserInteractor(user_repository=user_repository),
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
    )

    return app
