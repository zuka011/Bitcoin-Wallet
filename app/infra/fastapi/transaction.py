from typing import List

from core import BitcoinWalletService, Transaction
from fastapi import APIRouter, Depends, Header
from infra.fastapi.dependables import get_bitcoin_wallet_service
from infra.fastapi.exception_handlers import Error
from pydantic import BaseModel
from starlette import status


class TransactionModel(BaseModel):
    id: str
    source_address: str
    destination_address: str
    amount: float
    timestamp: str

    @staticmethod
    def get_from(transaction: Transaction) -> "TransactionModel":
        """Creates a new wallet model from the specified specified wallet."""
        return TransactionModel(
            id=transaction.id,
            source_address=transaction.source_address,
            destination_address=transaction.destination_address,
            amount=transaction.amount,
            timestamp=transaction.timestamp.isoformat(),
        )


class CreateTransactionRequest(BaseModel):
    source_address: str
    destination_address: str
    amount: float


class FetchTransactionsResponse(BaseModel):
    transactions: List[TransactionModel]


class FetchUserTransactionsResponse(BaseModel):
    transactions: List[TransactionModel]


transaction_api = APIRouter()


@transaction_api.post(
    path="/transactions",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"model": Error},
        status.HTTP_401_UNAUTHORIZED: {"model": Error},
    },
)
def create_transaction(
    request: CreateTransactionRequest,
    api_key: str = Header(""),
    core: BitcoinWalletService = Depends(get_bitcoin_wallet_service),
) -> None:
    """Transfers the given amount of funds from the specified source wallet to the destination one."""
    core.transfer(
        api_key=api_key,
        source_address=request.source_address,
        destination_address=request.destination_address,
        amount=request.amount,
    )


@transaction_api.get(
    path="/wallets/{address}/transactions",
    response_model=FetchTransactionsResponse,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": Error}},
)
def fetch_transactions(
    address: str,
    api_key: str = Header(""),
    core: BitcoinWalletService = Depends(get_bitcoin_wallet_service),
) -> FetchTransactionsResponse:
    """Retrieves all transactions associated with the specified wallet."""
    return FetchTransactionsResponse(
        transactions=[
            TransactionModel.get_from(transaction)
            for transaction in core.get_transactions(
                wallet_address=address, api_key=api_key
            )
        ]
    )


@transaction_api.get(
    path="/transactions",
    response_model=FetchUserTransactionsResponse,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": Error}},
)
def fetch_user_transactions(
    api_key: str = Header(""),
    core: BitcoinWalletService = Depends(get_bitcoin_wallet_service),
) -> FetchUserTransactionsResponse:
    """Retrieves all transactions associated with the user with the specified API key."""
    return FetchUserTransactionsResponse(
        transactions=[
            TransactionModel.get_from(transaction)
            for transaction in core.get_user_transactions(api_key=api_key)
        ]
    )
