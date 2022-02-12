from core import BitcoinWalletService, Wallet
from fastapi import APIRouter, Depends
from infra.fastapi.dependables import get_bitcoin_wallet_service
from infra.fastapi.response import Wrapped
from pydantic import BaseModel
from starlette import status


class WalletModel(BaseModel):
    address: str
    balance_btc: float
    balance_usd: float

    @staticmethod
    def get_from(wallet: Wallet) -> "WalletModel":
        """Creates a new wallet model from the specified specified wallet."""
        return WalletModel(
            address=wallet.address,
            balance_btc=wallet.balance_btc,
            balance_usd=wallet.balance_usd,
        )


class CreateWalletRequest(BaseModel):
    api_key: str


class CreateWalletResponse(BaseModel):
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
