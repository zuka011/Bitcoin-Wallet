from typing import Dict

from core import (
    BitcoinWalletService,
    Currency,
    InvalidApiKeyException,
    InvalidWalletRequestException,
    Wallet,
)
from fastapi import APIRouter, Depends, Header
from infra.fastapi.dependables import get_bitcoin_wallet_service
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


class WalletModel(BaseModel):
    address: str
    balance: Dict[Currency, float]

    @staticmethod
    def get_from(wallet: Wallet) -> "WalletModel":
        """Creates a new wallet model from the specified specified wallet."""
        return WalletModel(
            address=wallet.address,
            balance={
                Currency.BTC: wallet.get_balance(currency=Currency.BTC),
                Currency.USD: wallet.get_balance(currency=Currency.USD),
            },
        )


class CreateWalletRequest(BaseModel):
    pass


class CreateWalletResponse(BaseModel):
    wallet: WalletModel


class CreateWalletError(BaseModel):
    error_message: str


class FetchWalletRequest(BaseModel):
    pass


class FetchWalletResponse(BaseModel):
    wallet: WalletModel


class FetchWalletError(BaseModel):
    error_message: str


wallet_api = APIRouter()


@wallet_api.post(
    path="/wallets",
    response_model=CreateWalletResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_wallet(
    api_key: str = Header(""),
    core: BitcoinWalletService = Depends(get_bitcoin_wallet_service),
) -> CreateWalletResponse:
    """Creates a wallet for the user with the specified API key."""
    return CreateWalletResponse(
        wallet=WalletModel.get_from(core.create_wallet(api_key))
    )


@wallet_api.get(
    path="/wallets/{address}",
    response_model=FetchWalletResponse,
    status_code=status.HTTP_200_OK,
)
def fetch_wallet(
    address: str,
    api_key: str = Header(""),
    core: BitcoinWalletService = Depends(get_bitcoin_wallet_service),
) -> FetchWalletResponse:
    """Fetches the wallet at the specified address."""
    return FetchWalletResponse(
        wallet=WalletModel.get_from(core.get_wallet(address=address, api_key=api_key))
    )


def invalid_api_key_exception_handler(
    request: Request, exception: InvalidApiKeyException
) -> JSONResponse:
    """Exception handler for all InvalidApiKeyExceptions."""
    if request.method == "POST":
        content = CreateWalletError(error_message=str(exception)).dict()
    else:
        content = FetchWalletError(error_message=str(exception)).dict()

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=content,
    )


def invalid_wallet_request_exception_handler(
    _: Request, exception: InvalidWalletRequestException
) -> JSONResponse:
    """Exception handler for all InvalidWalletRequestExceptions."""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=CreateWalletError(error_message=str(exception)).dict(),
    )
