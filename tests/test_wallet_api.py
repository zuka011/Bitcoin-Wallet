from clients.user import UserClient
from clients.wallet import WalletClient
from core import Wallet
from infra import (
    CreateUserResponse,
    CreateWalletResponse,
    InMemoryWalletRepository,
    WalletModel,
)
from response_utils import parse_response
from starlette import status
from stubs.configuration import StubSystemConfiguration
from stubs.currency_converter import StubCurrencyConverter
from utils import random_string


def to_wallet(wallet: WalletModel) -> Wallet:
    """Converts the specified wallet model to a wallet."""
    return Wallet(
        address=wallet.address,
        balance_btc=wallet.balance_btc,
        balance_usd=wallet.balance_usd,
    )


def test_should_create_wallet_for_user(
    user_client: UserClient,
    wallet_client: WalletClient,
    memory_wallet_repository: InMemoryWalletRepository,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> None:
    api_key = parse_response(
        user_client.create_user(username=random_string()), CreateUserResponse
    ).api_key

    currency_converter.exchange_rate = 3
    system_configuration.initial_balance = 1

    response = wallet_client.create_wallet(api_key=api_key)
    wallet = to_wallet(parse_response(response, CreateWalletResponse).wallet)

    assert wallet.balance_btc == 1
    assert wallet.balance_usd == 3
    assert wallet == memory_wallet_repository.get_wallet(wallet_address=wallet.address)
    assert memory_wallet_repository.is_wallet_owner(
        wallet_address=wallet.address, api_key=api_key
    )

    assert response.status_code == status.HTTP_201_CREATED
