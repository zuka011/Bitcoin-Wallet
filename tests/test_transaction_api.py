import pytest
from clients.transaction import TransactionClient
from clients.user import UserClient
from clients.wallet import WalletClient
from core import Currency
from infra import (
    CreateUserResponse,
    CreateWalletResponse,
    FetchTransactionsResponse,
    FetchUserTransactionsResponse,
    FetchWalletResponse,
)
from response_utils import parse_response
from starlette import status
from stubs.configuration import StubSystemConfiguration
from stubs.currency_converter import StubCurrencyConverter
from utils import random_string


def test_should_create_transaction(
    user_client: UserClient,
    wallet_client: WalletClient,
    transaction_client: TransactionClient,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> None:
    currency_converter.btc_to_usd = 2
    system_configuration.initial_balance = 1
    system_configuration.same_user_transfer_fee = 50

    key = parse_response(
        user_client.create_user(random_string()), CreateUserResponse
    ).api_key
    wallet_address_1 = parse_response(
        wallet_client.create_wallet(api_key=key), CreateWalletResponse
    ).wallet.address
    wallet_address_2 = parse_response(
        wallet_client.create_wallet(api_key=key), CreateWalletResponse
    ).wallet.address

    response = transaction_client.create_transaction(
        api_key=key,
        source_address=wallet_address_1,
        destination_address=wallet_address_2,
        amount=1,
    )

    wallet_1 = parse_response(
        wallet_client.fetch_wallet(wallet_address=wallet_address_1, api_key=key),
        FetchWalletResponse,
    ).wallet
    wallet_2 = parse_response(
        wallet_client.fetch_wallet(wallet_address=wallet_address_2, api_key=key),
        FetchWalletResponse,
    ).wallet

    assert wallet_1.balance[Currency.BTC] == 0
    assert wallet_1.balance[Currency.USD] == 0
    assert wallet_2.balance[Currency.BTC] == 1.5
    assert wallet_2.balance[Currency.USD] == 3

    assert response.status_code == status.HTTP_201_CREATED


def test_should_fetch_transactions_for_wallet(
    user_client: UserClient,
    wallet_client: WalletClient,
    transaction_client: TransactionClient,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> None:
    currency_converter.btc_to_usd = 2
    system_configuration.initial_balance = 1
    system_configuration.same_user_transfer_fee = 0

    key = parse_response(
        user_client.create_user(random_string()), CreateUserResponse
    ).api_key
    wallet_address_1 = parse_response(
        wallet_client.create_wallet(api_key=key), CreateWalletResponse
    ).wallet.address
    wallet_address_2 = parse_response(
        wallet_client.create_wallet(api_key=key), CreateWalletResponse
    ).wallet.address

    transaction_client.create_transaction(
        api_key=key,
        source_address=wallet_address_1,
        destination_address=wallet_address_2,
        amount=1,
    )

    response_1 = transaction_client.fetch_transactions(
        wallet_address=wallet_address_1, api_key=key
    )
    response_2 = transaction_client.fetch_transactions(
        wallet_address=wallet_address_2, api_key=key
    )

    transactions_1 = parse_response(response_1, FetchTransactionsResponse).transactions
    transactions_2 = parse_response(response_2, FetchTransactionsResponse).transactions

    assert len(transactions_1) == 1
    assert len(transactions_2) == 1

    assert transactions_1[0].id == transactions_2[0].id
    assert transactions_1[0].source_address == wallet_address_1
    assert transactions_1[0].destination_address == wallet_address_2
    assert transactions_1[0].amount == 1
    assert transactions_1[0].timestamp == transactions_2[0].timestamp

    assert response_1.status_code == status.HTTP_200_OK
    assert response_2.status_code == status.HTTP_200_OK


def test_should_fetch_transactions_for_user(
    user_client: UserClient,
    wallet_client: WalletClient,
    transaction_client: TransactionClient,
    currency_converter: StubCurrencyConverter,
    system_configuration: StubSystemConfiguration,
) -> None:
    currency_converter.btc_to_usd = 2
    system_configuration.initial_balance = 1
    system_configuration.cross_user_transfer_fee = 10

    key_1 = parse_response(
        user_client.create_user(random_string()), CreateUserResponse
    ).api_key
    key_2 = parse_response(
        user_client.create_user(random_string()), CreateUserResponse
    ).api_key

    wallet_address_1 = parse_response(
        wallet_client.create_wallet(api_key=key_1), CreateWalletResponse
    ).wallet.address
    wallet_address_2 = parse_response(
        wallet_client.create_wallet(api_key=key_2), CreateWalletResponse
    ).wallet.address

    transaction_client.create_transaction(
        api_key=key_1,
        source_address=wallet_address_1,
        destination_address=wallet_address_2,
        amount=1,
    )

    response_1 = transaction_client.fetch_user_transactions(api_key=key_1)
    response_2 = transaction_client.fetch_user_transactions(api_key=key_2)
    transactions_1 = parse_response(
        response_1, FetchUserTransactionsResponse
    ).transactions
    transactions_2 = parse_response(
        response_2, FetchUserTransactionsResponse
    ).transactions

    assert len(transactions_1) == 2
    assert len(transactions_2) == 1

    assert transactions_1[0].id == transactions_2[0].id
    assert transactions_1[0].source_address == wallet_address_1
    assert transactions_1[0].destination_address == wallet_address_2
    assert transactions_1[0].amount == 0.9
    assert transactions_1[0].timestamp == transactions_2[0].timestamp

    assert transactions_1[1].source_address == wallet_address_1
    assert (
        transactions_1[1].destination_address
        == system_configuration.get_system_wallet_address()
    )
    assert transactions_1[1].amount == pytest.approx(0.1)

    assert response_1.status_code == status.HTTP_200_OK
    assert response_2.status_code == status.HTTP_200_OK
