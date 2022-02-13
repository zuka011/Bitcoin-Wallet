from core import (
    InvalidApiKeyException,
    InvalidUsernameException,
    InvalidWalletRequestException,
)
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


class Error(BaseModel):
    error_message: str


def invalid_username_exception_handler(
    _: Request, exception: InvalidUsernameException
) -> JSONResponse:
    """Exception handler for all InvalidUsernameExceptions."""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=Error(error_message=str(exception)).dict(),
    )


def invalid_api_key_exception_handler(
    _: Request, exception: InvalidApiKeyException
) -> JSONResponse:
    """Exception handler for all InvalidApiKeyExceptions."""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=Error(error_message=str(exception)).dict(),
    )


def invalid_wallet_request_exception_handler(
    _: Request, exception: InvalidWalletRequestException
) -> JSONResponse:
    """Exception handler for all InvalidWalletRequestExceptions."""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=Error(error_message=str(exception)).dict(),
    )
