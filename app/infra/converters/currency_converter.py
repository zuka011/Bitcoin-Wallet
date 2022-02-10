import requests

URL = "http://api.coinlayer.com/live"


class CoinLayerCurrencyConverter:
    @staticmethod
    def to_usd(btc: float) -> float:
        response = requests.request(
            "GET",
            URL,
            params={
                "access_key": "26f4a505fccdbd8501cd54b2fcbfe9d3",
                "target": "USD",
                "symbols": "BTC",
            },
        )
        rate = float(response.json()["rates"]["BTC"])
        return rate * btc
