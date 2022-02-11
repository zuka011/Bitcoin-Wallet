import string
from random import choice
from uuid import uuid4


def random_string(length: int = 10) -> str:
    """Creates a random string of the specified length."""
    return "".join([choice(string.ascii_letters) for _ in range(length)])


def random_api_key() -> str:
    """Returns a random API key as a string."""
    return str(uuid4())
