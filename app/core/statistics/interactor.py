from core.configurations import ISystemConfiguration
from core.repositories import IStatisticsRepository
from core.validators import InvalidApiKeyException


class StatisticsInteractor:
    def __init__(
        self,
        *,
        statistics_repository: IStatisticsRepository,
        system_configuration: ISystemConfiguration
    ) -> None:
        self.__statistics_repository = statistics_repository
        self.__system_configuration = system_configuration

    def get_total_transactions(self, *, api_key: str) -> int:
        """Returns the total number of performed transactions on the platform."""
        if api_key != self.__system_configuration.get_admin_api_key():
            raise InvalidApiKeyException("The specified Admin API key is incorrect.")

        return self.__statistics_repository.get_transactions()
