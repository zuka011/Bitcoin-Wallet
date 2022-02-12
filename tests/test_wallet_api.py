from clients.user import UserClient
from clients.wallet import WalletClient
from core import Currency
from infra import (
    CreateUserResponse,
    CreateWalletResponse,
    FetchWalletResponse,
    InMemoryWalletRepository,
)
from response_utils import parse_response
from starlette import status
from stubs.configuration import StubSystemConfiguration
from stubs.currency_converter import StubCurrencyConverter
from utils import random_string


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

    currency_converter.btc_to_usd = 3
    system_configuration.initial_balance = 1

    response = wallet_client.create_wallet(api_key=api_key)

    wallet = parse_response(response, CreateWalletResponse).wallet
    stored_wallet = memory_wallet_repository.get_wallet(wallet_address=wallet.address)

    assert wallet.balance[Currency.BTC] == 1
    assert wallet.balance[Currency.USD] == 3
    assert stored_wallet.balance == 1
    assert stored_wallet.currency == Currency.BTC
    assert memory_wallet_repository.is_wallet_owner(
        wallet_address=wallet.address, api_key=api_key
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_should_fetch_wallet(
    user_client: UserClient,
    wallet_client: WalletClient,
) -> None:
    api_key = parse_response(
        user_client.create_user(username=random_string()), CreateUserResponse
    ).api_key
    wallet = parse_response(
        wallet_client.create_wallet(api_key=api_key), CreateWalletResponse
    ).wallet

    response = wallet_client.fetch_wallet(
        wallet_address=wallet.address, api_key=api_key
    )
    fetched_wallet = parse_response(response, FetchWalletResponse).wallet

    assert wallet == fetched_wallet
