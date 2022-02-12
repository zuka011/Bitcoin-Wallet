from core import BitcoinWalletService
from fastapi import APIRouter, Depends
from infra.fastapi.dependables import get_bitcoin_wallet_service
from pydantic import BaseModel
from starlette import status


class CreateUserResponse(BaseModel):
    api_key: str


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
