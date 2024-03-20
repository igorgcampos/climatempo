from climatempo.application.controller import MapController
from climatempo.infra.city import ClimatempoAPI
from cloud_components.services.env.factory import EnvFactory
from cloud_components.infra.factory import InfraFactory
from cloud_components.services.log.builder import LogBuilder


if __name__ == "__main__":
    logger = LogBuilder().build_loguru()
    env = EnvFactory(logger=logger).manufacture_dotenv()
    env.load()

    factory = InfraFactory(logger=logger)
    aws = factory.manufacture_aws(
        access_key=env.get("AWS_ACCESS_KEY"),
        secret_access_key=env.get("AWS_SECRET_ACCESS_KEY"),
        env=env.get("ENV"),
        localstack_url=env.get("LOCALSTACK_URL"),
    )
    storage = aws.build_storage()
    storage.bucket = env.get("AWS_CLIMATEMPO_BUCKET")

    weather_api = ClimatempoAPI(env=env, logger=logger)

    map_controller = MapController(weather_api=weather_api, storage=storage, env=env)

    map_controller.build_tide_table()

    city_pkg = map_controller.list_cities()
    cities_weather = map_controller.get_forecast_by_cities(city_pkg=city_pkg)
    map_controller.build_map_template(cities_weather=cities_weather)
