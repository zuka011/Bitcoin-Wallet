from core import BitcoinWalletService
from fastapi import APIRouter, Depends
from infra.fastapi.dependables import get_bitcoin_wallet_service
from pydantic import BaseModel
from starlette import status


class FetchStatisticsRequest(BaseModel):
    api_key: str


class FetchStatisticsResponse(BaseModel):
    transactions: int
    total_profit: float


statistics_api = APIRouter()


@statistics_api.get(
    path="/statistics",
    response_model=FetchStatisticsResponse,
    status_code=status.HTTP_200_OK,
)
def fetch_statistics(
    request: FetchStatisticsRequest,
    core: BitcoinWalletService = Depends(get_bitcoin_wallet_service),
) -> FetchStatisticsResponse:
    """Returns the current transaction and profit statistics for the platform."""
    return FetchStatisticsResponse(
        transactions=core.get_total_transactions(api_key=request.api_key),
        total_profit=core.get_platform_profit(api_key=request.api_key),
    )
