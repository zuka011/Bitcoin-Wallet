from fastapi import APIRouter
from pydantic import BaseModel
from starlette import status


class FetchHelpResponse(BaseModel):
    help_message: str


help_api = APIRouter()


@help_api.get(
    path="/",
    response_model=FetchHelpResponse,
    status_code=status.HTTP_200_OK,
)
def fetch_help() -> FetchHelpResponse:
    """Returns a short help message for the API."""
    return FetchHelpResponse(
        help_message=(
            "Hello, this is a small Bitcoin Wallet server application.\n"
            "Currently it doesn't do much, but it will soon!\n"
        )
    )
