from infra import (
    CoinLayerCurrencyConverter,
    InMemoryUserRepository,
    InMemoryWalletRepository,
    SystemConfiguration,
)
from runner.web.setup import setup

app = setup(
    user_repository=InMemoryUserRepository(),
    wallet_repository=InMemoryWalletRepository(),
    currency_converter=CoinLayerCurrencyConverter(),
    system_configuration=SystemConfiguration(),
)
