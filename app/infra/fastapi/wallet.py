from fastapi import APIRouter
from infra import Wrapped
from pydantic import BaseModel


class CreateWalletRequest(BaseModel):
    api_key: str


class CreateWalletResponse(BaseModel):
    pass


wallet_api = APIRouter()


@wallet_api.post("/wallets")
def create_wallet(request: CreateWalletRequest) -> Wrapped[CreateWalletResponse]:
    """Creates a wallet for the user with the specified API key."""
