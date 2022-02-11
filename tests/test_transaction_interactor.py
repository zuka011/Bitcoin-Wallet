"""
Test List:
1) Should transfer funds from one wallet to another.    👾
2) Should update balance of wallets in all currencies.  👾
"""

from core import TransactionInteractor, UserInteractor, WalletInteractor
from infra import InMemoryWalletRepository
from stubs.balance_supplier import StubBalanceSupplier
from stubs.currency_converter import StubCurrencyConverter
from utils import random_string


def test_should_transfer_funds_for_user(
    user_interactor: UserInteractor,
    wallet_interactor: WalletInteractor,
    memory_wallet_repository: InMemoryWalletRepository,
    currency_converter: StubCurrencyConverter,
    balance_supplier: StubBalanceSupplier,
) -> None:
    currency_converter.exchange_rate = 2
    balance_supplier.initial_balance = 1

    transaction_interactor = TransactionInteractor(
        wallet_repository=memory_wallet_repository,
        currency_converter=currency_converter,
    )

    key = user_interactor.create_user(random_string())
    wallet_1 = wallet_interactor.create_wallet(api_key=key)
    wallet_2 = wallet_interactor.create_wallet(api_key=key)

    transaction_interactor.transfer(
        api_key=key,
        source_address=wallet_1.address,
        destination_address=wallet_2.address,
        amount_btc=0.5,
    )

    new_wallet_1 = wallet_interactor.get_wallet(address=wallet_1.address)
    new_wallet_2 = wallet_interactor.get_wallet(address=wallet_2.address)

    assert new_wallet_1.balance_btc == 0.5
    assert new_wallet_1.balance_usd == 1
    assert new_wallet_2.balance_btc == 1.5
    assert new_wallet_2.balance_usd == 3
