from fastapi import FastAPI
from infra import help_api


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(help_api)
    return app
