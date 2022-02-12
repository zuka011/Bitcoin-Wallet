from fastapi import APIRouter
from infra.fastapi.response import Wrapped
from pydantic import BaseModel
from starlette import status


class FetchHelpResponse(BaseModel):
    help_message: str


help_api = APIRouter()


@help_api.get(
    path="/",
    response_model=Wrapped[FetchHelpResponse],
    status_code=status.HTTP_200_OK,
)
def fetch_help() -> Wrapped[FetchHelpResponse]:
    """Returns a short help message for the API."""
    return Wrapped.from_response(
        FetchHelpResponse(
            help_message=(
                "Hello, this is a small Bitcoin Wallet server application.\n"
                "Currently it doesn't do much, but it will soon!\n"
            )
        )
    )
