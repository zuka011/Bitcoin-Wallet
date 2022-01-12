from fastapi import APIRouter
from infra.fastapi.response import ResponseStatus, Wrapped
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
    return Wrapped(
        status=ResponseStatus.SUCCESS,
        response=FetchHelpResponse(
            help_message=(
                "Hello, this is a small Bitcoin Wallet server application.\n"
                "Currently it doesn't do much, but it will soon!\n"
            )
        ),
    )
