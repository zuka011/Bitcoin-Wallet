from core import ICurrencyConverter
from core.repositories import IWalletRepository, Wallet


class TransactionInteractor:
    def __init__(
        self,
        *,
        wallet_repository: IWalletRepository,
        currency_converter: ICurrencyConverter
    ) -> None:
        self.__wallet_repository = wallet_repository
        self.__currency_converter = currency_converter

    def transfer(
        self,
        api_key: str,
        source_address: str,
        destination_address: str,
        amount_btc: float,
    ) -> None:
        source_wallet = self.__wallet_repository.get_wallet(
            wallet_address=source_address
        )
        destination_wallet = self.__wallet_repository.get_wallet(
            wallet_address=destination_address
        )

        updated_source_balance_btc = source_wallet.balance_btc - amount_btc
        updated_destination_balance_btc = destination_wallet.balance_btc + amount_btc

        self.__wallet_repository.update_wallet(
            Wallet(
                address=source_address,
                balance_btc=updated_source_balance_btc,
                balance_usd=self.__currency_converter.to_usd(
                    updated_source_balance_btc
                ),
            ),
            wallet_address=source_address,
        )
        self.__wallet_repository.update_wallet(
            Wallet(
                address=destination_address,
                balance_btc=updated_destination_balance_btc,
                balance_usd=self.__currency_converter.to_usd(
                    updated_destination_balance_btc
                ),
            ),
            wallet_address=destination_address,
        )
