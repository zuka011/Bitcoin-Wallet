from typing import Type, TypeVar

from pydantic import BaseModel
from requests.adapters import Response

T = TypeVar("T", bound=BaseModel, covariant=True)


def parse_response(response: Response, response_model: Type[T], /) -> T:
    """Parses the JSON content from the specified response based on the given response model."""
    return response_model.parse_obj(response.json())
