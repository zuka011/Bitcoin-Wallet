from core import (
    BitcoinWalletService,
    ICurrencyConverter,
    ISystemConfiguration,
    IUserRepository,
    IWalletRepository,
    UserInteractor,
    WalletInteractor,
)
from fastapi import FastAPI
from infra import help_api, user_api, wallet_api


def setup(
    *,
    user_repository: IUserRepository,
    wallet_repository: IWalletRepository,
    currency_converter: ICurrencyConverter,
    system_configuration: ISystemConfiguration
) -> FastAPI:
    app = FastAPI()
    app.include_router(help_api)
    app.include_router(user_api)
    app.include_router(wallet_api)

    app.state.core = BitcoinWalletService(
        user_interactor=UserInteractor(user_repository=user_repository),
        wallet_interactor=WalletInteractor(
            user_repository=user_repository,
            wallet_repository=wallet_repository,
            currency_converter=currency_converter,
            system_configuration=system_configuration,
        ),
    )

    return app
