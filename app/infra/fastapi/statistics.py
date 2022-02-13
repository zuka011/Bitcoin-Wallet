from core import BitcoinWalletService
from fastapi import APIRouter, Depends, Header
from infra.fastapi.dependables import get_bitcoin_wallet_service
from infra.fastapi.exception_handlers import Error
from pydantic import BaseModel
from starlette import status


class FetchStatisticsResponse(BaseModel):
    transactions: int
    total_profit: float


statistics_api = APIRouter()


@statistics_api.get(
    path="/statistics",
    response_model=FetchStatisticsResponse,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": Error}},
)
def fetch_statistics(
    api_key: str = Header(""),
    core: BitcoinWalletService = Depends(get_bitcoin_wallet_service),
) -> FetchStatisticsResponse:
    """Returns the current transaction and profit statistics for the platform."""
    return FetchStatisticsResponse(
        transactions=core.get_total_transactions(api_key=api_key),
        total_profit=core.get_platform_profit(api_key=api_key),
    )
