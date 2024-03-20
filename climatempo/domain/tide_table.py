import io
import json
import re
import zipfile
from cloud_components.application.interface.infra.storage import IStorage
from cloud_components.application.interface.services.enviroment.enviroment import (
    IEnviroment,
)
from typing import Dict, Iterable, Callable, List, Tuple


class Extractor:
    @staticmethod
    def split_forecast_time_value(time_value: str) -> Tuple[str]:
        time_value = time_value.split(" ")
        return time_value[0], time_value[-1]

    @staticmethod
    def format_time_from_tide_forecast(time: str) -> str:
        return f"{time[:2]}:{time[2:4]}"

    @staticmethod
    def get_month_day_and_week_day(tide: str) -> Tuple[str, str]:
        return (
            re.search(r"\d\d\n[DOM|SEG|TER|QUA|QUI|SEX|SAB]+", tide).group().split("\n")
        )

    @staticmethod
    def get_forecast(tide: str) -> List[str]:
        _, forecast = re.split(r"\d\d\n[DOM|SEG|TER|QUA|QUI|SEX|SAB]+", tide)
        forecast = forecast.split("\n")
        forecast = forecast[1:] if forecast[0] == "" else forecast
        return list(map(Extractor.split_forecast_time_value, forecast))

    @staticmethod
    def build_tide_table(
        forecast: List[str],
        tide_table: List[Dict[str, list]],
        month: str,
        month_day: str,
        week_day: str,
    ) -> Dict[str, list]:
        for time, tide_value in forecast:
            tide_table[month].append(
                {
                    "time": Extractor.format_time_from_tide_forecast(time),
                    "tide": tide_value,
                    "month_day": month_day,
                    "week_day": week_day,
                }
            )
        return tide_table

    @staticmethod
    def extract_tide_table(month: str, text: bytes) -> dict:
        if not text:
            return []
        tide_table = {}

        text = text.split("\n\n\n")
        month = text[0]
        tide_table[month] = []

        del text[0]
        for tide in text:
            month_day, week_day = Extractor.get_month_day_and_week_day(tide)
            try:
                forecast = Extractor.get_forecast(tide)
            except Exception as err:
                raise err
            tide_table = Extractor.build_tide_table(
                month=month,
                forecast=forecast,
                tide_table=tide_table,
                month_day=month_day,
                week_day=week_day,
            )
        return tide_table


class File:
    @staticmethod
    def get_file_from_s3(path: str, storage: IStorage) -> io.BytesIO:
        tide_forecast_zip = storage.get_file(file_path=path)
        return io.BytesIO(tide_forecast_zip)

    @staticmethod
    def open_tide_table_zip(
        buffer: io.BytesIO,
    ) -> Iterable[Tuple[zipfile.ZipFile, str]]:
        with zipfile.ZipFile(
            buffer, mode="a", compression=zipfile.ZIP_DEFLATED, allowZip64=False
        ) as file:
            for compressed_file_name in file.namelist():
                yield file, compressed_file_name

    @staticmethod
    def read_text_from_zip(file: zipfile.ZipFile, compressed_file_name: str):
        with file.open(compressed_file_name) as text:
            return text.read().decode("utf-8")

    @staticmethod
    def save_tide_table_in_json_file(tide_table: dict, storage: IStorage):
        json.dumps(tide_table, ensure_ascii=False)
        storage.save_file(
            data=json.dumps(tide_table, ensure_ascii=False),
            content_type="application/json",
            file_path="climatempo/tide/tide-table.json",
        )

    @staticmethod
    def cast_zip_to_json(buffer: bytes, extrac: Callable[[str, bytes], dict]) -> dict:
        tide_table = {}
        for compressed_file, compressed_file_name in File.open_tide_table_zip(buffer):
            month = compressed_file_name.replace(".txt", "")
            text = File.read_text_from_zip(
                file=compressed_file, compressed_file_name=compressed_file_name
            )
            tide_table.update(extrac(month, text))
        return tide_table


class TideTable:
    def __init__(self, storage: IStorage, env: IEnviroment) -> None:
        self.storage = storage
        self.env = env

    def build_tide_table(self):
        buffer = File.get_file_from_s3(self.env.get("TIDE_TABLE_ZIP"), self.storage)
        tide_table = File.cast_zip_to_json(
            buffer=buffer, extrac=Extractor.extract_tide_table
        )
        File.save_tide_table_in_json_file(tide_table, self.storage)
