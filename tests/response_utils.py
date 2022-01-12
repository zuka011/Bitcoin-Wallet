from typing import Type, TypeVar

from infra import ResponseStatus, Wrapped
from pydantic import BaseModel
from requests.adapters import Response

T = TypeVar("T", bound=BaseModel, covariant=True)


def parse_response(response: Response, response_model: Type[T], /) -> T:
    """Parses the JSON content from the specified response based on the given response model."""
    parsed_response: Wrapped[T] = Wrapped.parse_obj(response.json())

    assert parsed_response.status == ResponseStatus.SUCCESS
    assert parsed_response.response is not None

    return response_model.parse_obj(parsed_response.response)
