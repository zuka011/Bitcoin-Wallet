from typing import Dict

from core import BitcoinWalletService, Currency, Wallet
from fastapi import APIRouter, Depends
from infra.fastapi.dependables import get_bitcoin_wallet_service
from infra.fastapi.response import Wrapped
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


class CreateWalletRequest(BaseModel):
    api_key: str


class CreateWalletResponse(BaseModel):
    wallet: WalletModel


class FetchWalletRequest(BaseModel):
    api_key: str


class FetchWalletResponse(BaseModel):
    wallet: WalletModel


wallet_api = APIRouter()


@wallet_api.post(
    path="/wallets",
    response_model=Wrapped[CreateWalletResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_wallet(
    request: CreateWalletRequest,
    core: BitcoinWalletService = Depends(get_bitcoin_wallet_service),
) -> Wrapped[CreateWalletResponse]:
    """Creates a wallet for the user with the specified API key."""
    return Wrapped.from_response(
        CreateWalletResponse(
            wallet=WalletModel.get_from(core.create_wallet(request.api_key))
        )
    )


@wallet_api.get(
    path="/wallets/{address}",
    response_model=Wrapped[FetchWalletResponse],
    status_code=status.HTTP_200_OK,
)
def fetch_wallet(
    address: str,
    request: FetchWalletRequest,
    core: BitcoinWalletService = Depends(get_bitcoin_wallet_service),
) -> Wrapped[FetchWalletResponse]:
    """Fetches the wallet at the specified address."""
    return Wrapped.from_response(
        FetchWalletResponse(
            wallet=WalletModel.get_from(
                core.get_wallet(address=address, api_key=request.api_key)
            )
        )
    )
