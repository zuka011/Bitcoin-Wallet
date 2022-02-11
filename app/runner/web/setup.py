from core import BitcoinWalletService, IUserRepository, UserInteractor
from fastapi import FastAPI
from infra import help_api, user_api


def setup(*, user_repository: IUserRepository) -> FastAPI:
    app = FastAPI()
    app.include_router(help_api)
    app.include_router(user_api)

    app.state.core = BitcoinWalletService(
        user_interactor=UserInteractor(user_repository=user_repository)
    )

    return app
