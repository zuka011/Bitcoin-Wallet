from infra import CoinLayerCurrencyConverter, SystemConfiguration
from runner.web.setup import setup

app = setup(
    currency_converter=CoinLayerCurrencyConverter(),
    system_configuration=SystemConfiguration(),
)
