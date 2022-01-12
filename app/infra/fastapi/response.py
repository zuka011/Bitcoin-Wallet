from enum import Enum
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


class ResponseStatus(str, Enum):
    """An enumeration to specify whether a request was successful or not."""

    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


class Error(BaseModel):
    """A model for error related data."""

    message: str


ResponseT = TypeVar("ResponseT")


class Wrapped(GenericModel, Generic[ResponseT]):
    """Generic wrapper model for all FastAPI responses."""

    status: ResponseStatus
    response: Optional[ResponseT]
    error: Optional[Error]
