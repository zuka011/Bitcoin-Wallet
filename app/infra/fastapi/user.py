from core import BitcoinWalletService, InvalidUsernameException
from fastapi import APIRouter, Depends
from infra.fastapi.dependables import get_bitcoin_wallet_service
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


class CreateUserResponse(BaseModel):
    api_key: str


class CreateUserError(BaseModel):
    error_message: str


user_api = APIRouter()


@user_api.post(
    path="/users/{username}",
    response_model=CreateUserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    username: str, core: BitcoinWalletService = Depends(get_bitcoin_wallet_service)
) -> CreateUserResponse:
    """Creates a user with the specified username."""
    return CreateUserResponse(api_key=core.create_user(username))


def invalid_username_exception_handler(
    _: Request, exception: InvalidUsernameException
) -> JSONResponse:
    """Exception handler for all InvalidUsernameExceptions."""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=CreateUserError(error_message=str(exception)).dict(),
    )
