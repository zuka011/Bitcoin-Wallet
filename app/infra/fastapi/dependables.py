from typing import cast

from core import BitcoinWalletService
from starlette.requests import Request


def get_bitcoin_wallet_service(request: Request) -> BitcoinWalletService:
    """Returns the core service of the system from the app's state."""
    return cast(BitcoinWalletService, request.app.state.core)
