from clients.statistics import StatisticsClient
from clients.transaction import TransactionClient
from clients.user import UserClient
from clients.wallet import WalletClient
from infra import CreateUserResponse, CreateWalletResponse, FetchStatisticsResponse
from response_utils import parse_response
from starlette import status
from stubs.configuration import StubSystemConfiguration
from utils import random_string


def test_should_return_empty_platform_statistics(
    statistics_client: StatisticsClient, system_configuration: StubSystemConfiguration
) -> None:
    response = statistics_client.fetch_statistics(
        api_key=system_configuration.admin_api_key
    )
    statistics = parse_response(response, FetchStatisticsResponse)

    assert statistics.transactions == 0
    assert statistics.total_profit == 0

    assert response.status_code == status.HTTP_200_OK


def test_should_return_platform_statistics(
    user_client: UserClient,
    wallet_client: WalletClient,
    transaction_client: TransactionClient,
    statistics_client: StatisticsClient,
    system_configuration: StubSystemConfiguration,
) -> None:
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

    response = statistics_client.fetch_statistics(
        api_key=system_configuration.admin_api_key
    )
    statistics = parse_response(response, FetchStatisticsResponse)

    assert statistics.transactions == 2
    assert statistics.total_profit == 0.1

    assert response.status_code == status.HTTP_200_OK
