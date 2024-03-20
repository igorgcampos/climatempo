from typing import Dict, Literal


CityType = Dict[Literal["id", "name", "state", "country"], str | int | float]

CityPackageType = Dict[
    Literal["city", "cities_qtde", "city_index", "pkg_id"], CityType | int | str
]

WeatherType = Dict[Literal["id", "name", "state", "country", "data"], int | str | list]

ForecastType = Dict[
    Literal["city", "cities_qtde", "city_index", "pkg_id", "weather"], int | str
]
