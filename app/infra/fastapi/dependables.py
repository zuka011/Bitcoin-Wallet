from typing import cast

from core import BitcoinWalletService
from starlette.requests import Request


def get_bitcoin_wallet_service(request: Request) -> BitcoinWalletService:
    return cast(BitcoinWalletService, request.app.state.core)
