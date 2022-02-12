import requests
from core import Currency

URL = "https://api.nomics.com/v1/exchange-rates"


class CoinLayerCurrencyConverter:
    @staticmethod
    def convert(amount: float, *, source: Currency, target: Currency) -> float:
        """Converts the specified amount of the source currency to the target."""
        assert (
            target == Currency.USD
        ), f"Cannot convert to currencies other than {Currency.USD}."

        response = requests.get(
            URL,
            params={
                "key": "12d10c6f43b7d4babf0c0f42d5ff7cfc8afc38a0",
            },
        )
        rates = dict((rate["currency"], rate["rate"]) for rate in response.json())
        assert source in rates, f"There is not data on the currency {source}."

        rate = float(rates[source])
        return amount * rate
