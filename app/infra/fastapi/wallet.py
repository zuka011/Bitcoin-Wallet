from typing import Dict

from core import BitcoinWalletService, Currency, Wallet
from fastapi import APIRouter, Depends, Header
from infra.fastapi.dependables import get_bitcoin_wallet_service
from infra.fastapi.exception_handlers import Error
from pydantic import BaseModel
from starlette import status


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


class CreateWalletResponse(BaseModel):
    wallet: WalletModel


class FetchWalletResponse(BaseModel):
    wallet: WalletModel


wallet_api = APIRouter()


@wallet_api.post(
    path="/wallets",
    response_model=CreateWalletResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"model": Error},
        status.HTTP_401_UNAUTHORIZED: {"model": Error},
    },
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
    responses={status.HTTP_401_UNAUTHORIZED: {"model": Error}},
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
