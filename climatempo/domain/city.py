from typing import List
from climatempo.application.interfaces.infra import IWeatherAPI
from climatempo.application.types import CityPackageType
from climatempo.services.executor import execute_on_interval


class City:
    def __init__(self, weather_api: IWeatherAPI) -> None:
        self.weather_api = weather_api

    def get_forercast_from_city_pkg(self, cities_pkg: List[CityPackageType]):
        return execute_on_interval(
            interval_in_seconds=60,
            to_execute_in_interval=10,
            executables=[
                (self.weather_api.get_weather_from_city, city)
                for _, city in enumerate(cities_pkg)
            ],
        )
