from abc import ABC, abstractmethod
from typing import List
from climatempo.application.types import CityType


class IWeatherAPI(ABC):
    @abstractmethod
    def list_cities(
        self,
    ) -> List[CityType] | None:
        raise NotImplementedError

    @abstractmethod
    def get_weather_from_city(self, city: int):
        raise NotImplementedError
