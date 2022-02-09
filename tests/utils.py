import string
from random import choice


def random_string(length: int = 10) -> str:
    """Creates a random string."""
    return "".join([choice(string.ascii_letters) for _ in range(length)])
