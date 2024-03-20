import requests
import json
from typing import List
from climatempo.application.types import CityType
from climatempo.application.interfaces.infra import IWeatherAPI
from cloud_components.application.interface.services.enviroment.enviroment import (
    IEnviroment,
)
from cloud_components.application.interface.services.log.logger import ILogger


class ClimatempoAPI(IWeatherAPI):
    def __init__(self, env: IEnviroment, logger: ILogger) -> None:
        self.env = env
        self.logger = logger

    def list_cities(
        self,
    ) -> List[CityType] | None:
        target = (
            self.env.get("CLIMATEMPO_URL")
            + "/api-manager/user-token/"
            + self.env.get("CLIMATEMPO_API_KEY")
            + "/locales"
        )
        self.logger.info(f"Listing cities from {target}")
        response = requests.get(target, timeout=15)
        if not response.status_code == 200:
            return None
        content = response.json()
        return content.get("locales")

    def get_weather_from_city(self, city: int):
        self.logger.info(f"Getting weather from city {city}")
        api_key = self.env.get("CLIMATEMPO_API_KEY")
        api_url = self.env.get("CLIMATEMPO_URL")
        response = requests.get(
            url=f"{api_url}/api/v1/forecast/locale/{city}/days/15?token={api_key}",
            timeout=15,
        )
        self.logger.info(f"Response code {response.status_code} from city {city}")
        if response.status_code >= 200 and response.status_code <= 299:
            return response.json()
