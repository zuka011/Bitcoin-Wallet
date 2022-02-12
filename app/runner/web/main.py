from infra import (
    CoinLayerCurrencyConverter,
    InMemoryStatisticsRepository,
    InMemoryTransactionRepository,
    InMemoryUserRepository,
    InMemoryWalletRepository,
    SystemConfiguration,
)
from runner.web.setup import setup

wallet_repository = InMemoryWalletRepository()

app = setup(
    user_repository=InMemoryUserRepository(),
    wallet_repository=wallet_repository,
    transaction_repository=InMemoryTransactionRepository(
        wallet_repository=wallet_repository
    ),
    statistics_repository=InMemoryStatisticsRepository(),
    currency_converter=CoinLayerCurrencyConverter(),
    system_configuration=SystemConfiguration(),
)
