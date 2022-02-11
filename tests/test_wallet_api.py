from clients.user import UserClient
from clients.wallet import WalletClient
from utils import random_string


def test_should_create_wallet_for_user(
    user_client: UserClient, wallet_client: WalletClient
) -> None:
    user_client.create_user(random_string())

    wallet_client
