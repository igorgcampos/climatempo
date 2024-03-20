from typing import List
from climatempo.application.interfaces.infra import IWeatherAPI
from climatempo.application.types import CityPackageType, ForecastType
from climatempo.domain.city import City
from climatempo.domain.map import build_map_template
from cloud_components.application.interface.infra.storage import IStorage
from climatempo.application.interfaces.scheduler import IScheduler
from climatempo.domain.tide_table import TideTable
from cloud_components.application.interface.services.enviroment.enviroment import (
    IEnviroment,
)


class MapController:
    def __init__(
        self, weather_api: IWeatherAPI, storage: IStorage, env: IEnviroment
    ) -> None:
        self.weather_api = weather_api
        self.storage = storage
        self.city = City(weather_api=weather_api)
        self.tide_table = TideTable(storage=storage, env=env)

    def list_cities(self) -> CityPackageType:
        return self.weather_api.list_cities()

    def get_forecast_by_cities(
        self, city_pkg: List[CityPackageType]
    ) -> List[ForecastType]:
        return self.city.get_forercast_from_city_pkg(city_pkg)

    def build_map_template(self, cities_weather: List[ForecastType]) -> None:
        build_map_template(weather=cities_weather, storage=self.storage)

    def build_tide_table(self):
        self.tide_table.build_tide_table()


class SchedulerController:
    def __init__(self, map_controller: MapController, scheduler: IScheduler) -> None:
        self.map_controller = map_controller
        self.scheduler = scheduler

    def tide_table_scheduler(self) -> None:
        self.scheduler.schedule(
            every="minutes", at=5, do=self.map_controller.build_tide_table
        )

    def map_scheduler(self) -> None:
        self.scheduler.schedule(
            every="day",
            at="09:00",
            timezone="America/Sao_Paulo",
            do=lambda: self.map_controller.build_map_template(
                cities_weather=self.map_controller.get_forecast_by_cities(
                    city_pkg=self.map_controller.list_cities()
                )
            ),
        )
