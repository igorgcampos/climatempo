# Lib que acessa a ownCloud, aqui estao todos os mapas de calor do brasil e rio de janeiro
# https://pypi.org/project/pyocclient/
import json
import os
import datetime
from typing import List
import ephem
from unidecode import unidecode
from cloud_components.application.interface.infra.storage import IStorage
from bs4 import BeautifulSoup
from loguru import logger

from climatempo.application.types import ForecastType

ICON_PATH = "file:///E:/Jornais/oglobo/icones"
ENV = os.getenv("ENV", "local")

if ENV == "local":
    from dotenv import load_dotenv

    load_dotenv()


def format_moon_date(moon_date: int):
    date = ephem.localtime(moon_date)
    return date.strftime("%d/%m")


def get_next_new_moon(date: datetime.datetime.date):
    date = ephem.Date(date)
    new_moon = ephem.next_new_moon(date)
    return format_moon_date(moon_date=new_moon)


def get_next_first_quarter_moon(date: datetime.datetime.date):
    date = ephem.Date(date)
    first_quarter = ephem.next_first_quarter_moon(date)
    return format_moon_date(moon_date=first_quarter)


def get_next_full_moon(date: datetime.datetime.date):
    date = ephem.Date(date)
    full_moon = ephem.next_full_moon(date)
    return format_moon_date(moon_date=full_moon)


def get_next_last_quarter_moon(date: datetime.datetime.date):
    date = ephem.Date(date)
    last_quarter = ephem.next_last_quarter_moon(date=date)
    return format_moon_date(moon_date=last_quarter)


def normalize_name(name: str, first_letter_upper: bool):
    name = unidecode(name)
    splited_name = name.split()
    splited_name = [name[0].upper() + name[1:] for name in splited_name]
    name = "".join(splited_name)
    if not first_letter_upper:
        return name[0].lower() + name[1:]
    return name[0].upper() + name[1:]


def change_weather_value(
    city: str, type: str, value: str, template: BeautifulSoup, first_letter_upper=False
) -> BeautifulSoup:
    if city == "Rio de Janeiro":
        pass
    if city:
        city = normalize_name(name=city, first_letter_upper=first_letter_upper)
    try:
        tag = template.find(f"{city}{type}")
        p_tag = tag.find("p")
        if p_tag:
            p_tag.string = value
        else:
            tag.string = value
    except Exception as err:
        pass
    return template


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def open_weather_template():
    with open(
        f"{os.getenv('CLIMATEMPO_PROJECT_PATH')}/assets/template.xml",
        "r",
        encoding="utf-8",
    ) as file:
        data = file.read()
    return BeautifulSoup(data, "xml")


def save_completed_template(template: BeautifulSoup, storage: IStorage):
    template = str(template)
    template = template.replace(
        '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20001102//EN" "http://www.w3.org/TR/2000/CR-SVG-20001102/DTD/svg-20001102.dtd">',
        "",
    )
    template = template.replace(
        '<?xml version="1.0" encoding="utf-8"?>',
        """
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20001102//EN" "http://www.w3.org/TR/2000/CR-SVG-20001102/DTD/svg-20001102.dtd" [
    <!ENTITY ns_graphs "http://ns.adobe.com/Graphs/1.0/">
    <!ENTITY ns_vars "http://ns.adobe.com/Variables/1.0/">
    <!ENTITY ns_imrep "http://ns.adobe.com/ImageReplacement/1.0/">
    <!ENTITY ns_custom "http://ns.adobe.com/GenericCustomNamespace/1.0/">
    <!ENTITY ns_flows "http://ns.adobe.com/Flows/1.0/">
    <!ENTITY ns_extend "http://ns.adobe.com/Extensibility/1.0/">
]>
    """,
    )
    storage.save_file(
        data=template[1:],
        file_path="climatempo/template.xml",
        content_type="application/octet-stream",
        is_public=True,
    )
    # s3.save_text_file(file_path="template.xml", data=str(template), is_public=True)


def thermal_sensation(city: dict, weather_template: BeautifulSoup):
    weather = city["data"]
    city_name = city["name"]
    # -------------------- min thermal sensation --------------------
    weather_template = change_weather_value(
        type="SensacaoTermicaMinimaPrimeiroDia",
        city=city_name,
        value=f"{weather[0]['thermal_sensation']['min']}°",
        template=weather_template,
    )
    weather_template = change_weather_value(
        type="SensacaoTermicaMinimaSegundoDia",
        city=city_name,
        value=f"{weather[1]['thermal_sensation']['min']}°",
        template=weather_template,
    )
    weather_template = change_weather_value(
        type="SensacaoTermicaMinimaTerceiroDia",
        city=city_name,
        value=f"{weather[2]['thermal_sensation']['min']}°",
        template=weather_template,
    )
    weather_template = change_weather_value(
        type="SensacaoTermicaMinimaQuartoDia",
        city=city_name,
        value=f"{weather[3]['thermal_sensation']['min']}°",
        template=weather_template,
    )
    weather_template = change_weather_value(
        type="SensacaoTermicaMinimaQuintoDia",
        city=city_name,
        value=f"{weather[4]['thermal_sensation']['min']}°",
        template=weather_template,
    )
    weather_template = change_weather_value(
        type="SensacaoTermicaMinimaSextoDia",
        city=city_name,
        value=f"{weather[5]['thermal_sensation']['min']}°",
        template=weather_template,
    )
    weather_template = change_weather_value(
        type="SensacaoTermicaMinimaSetimoDia",
        city=city_name,
        value=f"{weather[6]['thermal_sensation']['min']}°",
        template=weather_template,
    )
    # -------------------- max thermal sensation --------------------
    weather_template = change_weather_value(
        type="SensacaoTermicaMaximaPrimeiroDia",
        city=city_name,
        value=f"{weather[0]['thermal_sensation']['max']}°",
        template=weather_template,
    )
    weather_template = change_weather_value(
        type="SensacaoTermicaMaximaSegundoDia",
        city=city_name,
        value=f"{weather[1]['thermal_sensation']['max']}°",
        template=weather_template,
    )
    weather_template = change_weather_value(
        type="SensacaoTermicaMaximaTerceiroDia",
        city=city_name,
        value=f"{weather[2]['thermal_sensation']['max']}°",
        template=weather_template,
    )
    weather_template = change_weather_value(
        type="SensacaoTermicaMaximaQuartoDia",
        city=city_name,
        value=f"{weather[3]['thermal_sensation']['max']}°",
        template=weather_template,
    )
    weather_template = change_weather_value(
        type="SensacaoTermicaMaximaQuintoDia",
        city=city_name,
        value=f"{weather[4]['thermal_sensation']['max']}°",
        template=weather_template,
    )
    weather_template = change_weather_value(
        type="SensacaoTermicaMaximaSextoDia",
        city=city_name,
        value=f"{weather[5]['thermal_sensation']['max']}°",
        template=weather_template,
    )
    weather_template = change_weather_value(
        type="SensacaoTermicaMaximaSetimoDia",
        city=city_name,
        value=f"{weather[6]['thermal_sensation']['max']}°",
        template=weather_template,
    )
    return weather_template


def temperature(city: dict, weather_template: BeautifulSoup):
    weather = city["data"][0]
    city_name = city["name"]
    weather_template = change_weather_value(
        city=city_name,
        type="TemperaturaMaxima",
        value=f"{weather['temperature']['max']}°",
        template=weather_template,
    )
    weather_template = change_weather_value(
        type="TemperaturaMinima",
        city=city_name,
        value=f"{weather['temperature']['min']}°",
        template=weather_template,
    )
    weather_template = change_weather_value(
        city=city_name,
        type="TemperaturaMaxima2",
        value=f"{weather['temperature']['max']}°",
        template=weather_template,
    )
    weather_template = change_weather_value(
        type="TemperaturaMinima2",
        city=city_name,
        value=f"{weather['temperature']['min']}°",
        template=weather_template,
    )
    return weather_template


def rain_probability_icon(city: dict, weather_template: BeautifulSoup):
    icon_name = city["data"][0]["text_icon"]["icon"]["day"]
    return change_weather_value(
        type="Icone",
        city=city["name"],
        value=f"{ICON_PATH}/ico{icon_name}.ai",
        template=weather_template,
    )


def rain_probability_in_rj_week(city: dict, weather_template: BeautifulSoup):
    day_index = {
        0: "ProbabilidadeDeChuvaPrimeiroDia",
        1: "ProbabilidadeDeChuvaSegundoDia",
        2: "ProbabilidadeDeChuvaTerceiroDia",
        3: "ProbabilidadeDeChuvaQuartoDia",
        4: "ProbabilidadeDeChuvaQuintoDia",
        5: "ProbabilidadeDeChuvaSextoDia",
        6: "ProbabilidadeDeChuvaSetimoDia",
    }
    if city["name"] == "Rio de Janeiro" and city["id"] == 5959:
        data = city["data"][0:7]
        for index in range(0, 7):
            if data[index]["rain"]["probability"] < 10:
                rain_probability = "BAIXA"
            if (
                data[index]["rain"]["probability"] >= 10
                and data[index]["rain"]["probability"] < 40
            ):
                rain_probability = "MEDIA"
            if data[index]["rain"]["probability"] > 40:
                rain_probability = "ALTA"
            weather_template = change_weather_value(
                type=day_index[index],
                city=city["name"],
                value=rain_probability,
                template=weather_template,
            )
    return weather_template


def max_and_min_temperature_in_rj(city: dict, weather_template: BeautifulSoup):
    # Rio de Janeiro -> Zona Sul
    # Duque de Caxias -> Zona Norte
    # Itaguaí -> Zona Oeste
    temperature_index = {
        "minima": {
            "Itaguaí": {
                0: "ZonaOesteTemperaturaMinimaPrimeiroDia",
                1: "ZonaOesteTemperaturaMinimaSegundoDia",
                2: "ZonaOesteTemperaturaMinimaTerceiroDia",
                3: "ZonaOesteTemperaturaMinimaQuartoDia",
                4: "ZonaOesteTemperaturaMinimaQuintoDia",
                5: "ZonaOesteTemperaturaMinimaSextoDia",
                6: "ZonaOesteTemperaturaMinimaSetimoDia",
            },
            "Rio de Janeiro": {
                0: "ZonaSulTemperaturaMinimaPrimeiroDia",
                1: "ZonaSulTemperaturaMinimaSegundoDia",
                2: "ZonaSulTemperaturaMinimaTerceiroDia",
                3: "ZonaSulTemperaturaMinimaQuartoDia",
                4: "ZonaSulTemperaturaMinimaQuintoDia",
                5: "ZonaSulTemperaturaMinimaSextoDia",
                6: "ZonaSulTemperaturaMinimaSetimoDia",
            },
            "Duque de Caxias": {
                0: "ZonaNorteTemperaturaMinimaPrimeiroDia",
                1: "ZonaNorteTemperaturaMinimaSegundoDia",
                2: "ZonaNorteTemperaturaMinimaTerceiroDia",
                3: "ZonaNorteTemperaturaMinimaQuartoDia",
                4: "ZonaNorteTemperaturaMinimaQuintoDia",
                5: "ZonaNorteTemperaturaMinimaSextoDia",
                6: "ZonaNorteTemperaturaMinimaSetimoDia",
            },
        },
        "maxima": {
            "Itaguaí": {
                0: "ZonaOesteTemperaturaMaximaPrimeiroDia",
                1: "ZonaOesteTemperaturaMaximaSegundoDia",
                2: "ZonaOesteTemperaturaMaximaTerceiroDia",
                3: "ZonaOesteTemperaturaMaximaQuartoDia",
                4: "ZonaOesteTemperaturaMaximaQuintoDia",
                5: "ZonaOesteTemperaturaMaximaSextoDia",
                6: "ZonaOesteTemperaturaMaximaSetimoDia",
            },
            "Rio de Janeiro": {
                0: "ZonaSulTemperaturaMaximaPrimeiroDia",
                1: "ZonaSulTemperaturaMaximaSegundoDia",
                2: "ZonaSulTemperaturaMaximaTerceiroDia",
                3: "ZonaSulTemperaturaMaximaQuartoDia",
                4: "ZonaSulTemperaturaMaximaQuintoDia",
                5: "ZonaSulTemperaturaMaximaSextoDia",
                6: "ZonaSulTemperaturaMaximaSetimoDia",
            },
            "Duque de Caxias": {
                0: "ZonaNorteTemperaturaMaximaPrimeiroDia",
                1: "ZonaNorteTemperaturaMaximaSegundoDia",
                2: "ZonaNorteTemperaturaMaximaTerceiroDia",
                3: "ZonaNorteTemperaturaMaximaQuartoDia",
                4: "ZonaNorteTemperaturaMaximaQuintoDia",
                5: "ZonaNorteTemperaturaMaximaSextoDia",
                6: "ZonaNorteTemperaturaMaximaSetimoDia",
            },
        },
    }
    city_name = city["name"]
    if city_name in ["Rio de Janeiro", "Duque de Caxias", "Itaguaí"]:
        data = city["data"][0:7]
        for index in range(0, 7):
            weather_template = change_weather_value(
                type=temperature_index["maxima"][city_name][index],
                city="Rio de Janeiro",
                value=f"{data[index]['temperature']['max']}°",
                template=weather_template,
            )
            weather_template = change_weather_value(
                type=temperature_index["minima"][city_name][index],
                city="Rio de Janeiro",
                value=f"{data[index]['temperature']['min']}°",
                template=weather_template,
            )
    return weather_template


def sunrise_and_sunset_in_rj(city: dict, weather_template: BeautifulSoup):
    def format_time_string(time_string: str):
        time_string = time_string.split(":")
        return f"{time_string[0]}H{time_string[1]}"

    if city["name"] == "Rio de Janeiro" and city["id"] == 5959:
        sunrise = format_time_string(city["data"][0]["sun"]["sunrise"])
        sunset = format_time_string(city["data"][0]["sun"]["sunset"])
        weather_template = change_weather_value(
            type="NascerDoSol",
            city=city["name"],
            value=sunrise,
            template=weather_template,
            first_letter_upper=True,
        )
        weather_template = change_weather_value(
            type="PorDoSol",
            city=city["name"],
            value=sunset,
            template=weather_template,
            first_letter_upper=True,
        )
    return weather_template


def moon_phases(weather_template: BeautifulSoup):
    _date = datetime.datetime.now().date()
    weather_template = change_weather_value(
        type="dataLuaNova",
        city="",
        value=get_next_new_moon(date=_date),
        template=weather_template,
        first_letter_upper=False,
    )
    weather_template = change_weather_value(
        type="dataLuaCrescente",
        city="",
        value=get_next_first_quarter_moon(date=_date),
        template=weather_template,
        first_letter_upper=True,
    )
    weather_template = change_weather_value(
        type="dataLuaCheia",
        city="",
        value=get_next_full_moon(date=_date),
        template=weather_template,
        first_letter_upper=True,
    )
    weather_template = change_weather_value(
        type="dataLuaMinguante",
        city="",
        value=get_next_last_quarter_moon(date=_date),
        template=weather_template,
        first_letter_upper=True,
    )
    return weather_template


def temperature_in_rj_zones(city: dict, weather_template: BeautifulSoup):
    # Rio de Janeiro -> Zona Sul
    # Duque de Caxias -> Zona Norte
    # Itaguaí -> Zona Oeste
    zone_index = {
        "Rio de Janeiro": {
            "maxima": {
                0: "ZonaSulTemperaturaMaximaPrimeiroDia",
                1: "ZonaSulTemperaturaMaximaSegundoDia",
                2: "ZonaSulTemperaturaMaximaTerceiroDia",
                3: "ZonaSulTemperaturaMaximaQuartoDia",
                4: "ZonaSulTemperaturaMaximaQuintoDia",
                5: "ZonaSulTemperaturaMaximaSextoDia",
                6: "ZonaSulTemperaturaMaximaSetimoDia",
            },
            "minima": {
                0: "ZonaSulTemperaturaMinimaPrimeiroDia",
                1: "ZonaSulTemperaturaMinimaSegundoDia",
                2: "ZonaSulTemperaturaMinimaTerceiroDia",
                3: "ZonaSulTemperaturaMinimaQuartoDia",
                4: "ZonaSulTemperaturaMinimaQuintoDia",
                5: "ZonaSulTemperaturaMinimaSextoDia",
                6: "ZonaSulTemperaturaMinimaSetimoDia",
            },
        },
        "Duque de Caxias": {
            "maxima": {
                0: "ZonaNorteTemperaturaMaximaPrimeiroDia",
                1: "ZonaNorteTemperaturaMaximaSegundoDia",
                2: "ZonaNorteTemperaturaMaximaTerceiroDia",
                3: "ZonaNorteTemperaturaMaximaQuartoDia",
                4: "ZonaNorteTemperaturaMaximaQuintoDia",
                5: "ZonaNorteTemperaturaMaximaSextoDia",
                6: "ZonaNorteTemperaturaMaximaSetimoDia",
            },
            "minima": {
                0: "ZonaNorteTemperaturaMinimaPrimeiroDia",
                1: "ZonaNorteTemperaturaMinimaSegundoDia",
                2: "ZonaNorteTemperaturaMinimaTerceiroDia",
                3: "ZonaNorteTemperaturaMinimaQuartoDia",
                4: "ZonaNorteTemperaturaMinimaQuintoDia",
                5: "ZonaNorteTemperaturaMinimaSextoDia",
                6: "ZonaNorteTemperaturaMinimaSetimoDia",
            },
        },
        "Itaguaí": {
            "maxima": {
                0: "ZonaOesteTemperaturaMaximaPrimeiroDia",
                1: "ZonaOesteTemperaturaMaximaSegundoDia",
                2: "ZonaOesteTemperaturaMaximaTerceiroDia",
                3: "ZonaOesteTemperaturaMaximaQuartoDia",
                4: "ZonaOesteTemperaturaMaximaQuintoDia",
                5: "ZonaOesteTemperaturaMaximaSextoDia",
                6: "ZonaOesteTemperaturaMaximaSetimoDia",
            },
            "minima": {
                0: "ZonaOesteTemperaturaMinimaPrimeiroDia",
                1: "ZonaOesteTemperaturaMinimaSegundoDia",
                2: "ZonaOesteTemperaturaMinimaTerceiroDia",
                3: "ZonaOesteTemperaturaMinimaQuartoDia",
                4: "ZonaOesteTemperaturaMinimaQuintoDia",
                5: "ZonaOesteTemperaturaMinimaSextoDia",
                6: "ZonaOesteTemperaturaMinimaSetimoDia",
            },
        },
    }
    city_name = city["name"]
    if city_name in ["Rio de Janeiro", "Duque de Caxias", "Itaguaí"]:
        weather = city["data"][0:7]
        for index in range(0, 7):
            maximum = zone_index[city_name]["maxima"][index]
            minimum = zone_index[city_name]["minima"][index]
            weather_template = change_weather_value(
                type=maximum,
                city="Rio De Janeiro",
                value=f"{weather[index]['temperature']['max']}°",
                template=weather_template,
            )
            weather_template = change_weather_value(
                type=minimum,
                city="Rio De Janeiro",
                value=f"{weather[index]['temperature']['min']}°",
                template=weather_template,
            )
    return weather_template


def rj_tide_table(tide_table: dict, weather_template: BeautifulSoup) -> BeautifulSoup:
    months = {
        1: "JANEIRO",
        2: "FEVEREIRO",
        3: "MARÇO",
        4: "ABRIL",
        5: "MAIO",
        6: "JUNHO",
        7: "JULHO",
        8: "AGOSTO",
        9: "SETEMBRO",
        10: "OUTUBRO",
        11: "NOVEMBRO",
        12: "DEZEMBRO",
    }
    now = datetime.datetime.now()
    tide_table = tide_table[months[now.month]]
    tide_table = [tide for tide in tide_table if int(tide["month_day"]) == now.day][:4]
    # dataset = weather_template.find("sampleDataSet")
    icon = None
    if float(tide_table[0]["tide"]) >= 1 and len(tide_table) == 3:
        icon = f"{ICON_PATH}/marealta2.ai"
    if float(tide_table[0]["tide"]) < 1 and len(tide_table) == 3:
        icon = f"{ICON_PATH}/marebaixa2.ai"
    if float(tide_table[0]["tide"]) >= 1 and len(tide_table) == 4:
        icon = f"{ICON_PATH}/marealta.ai"
    if float(tide_table[0]["tide"]) < 1 and len(tide_table) == 4:
        icon = f"{ICON_PATH}/marebaixa.ai"
    for index in range(len(tide_table)):  # pylint: disable=C0200
        number = index + 1
        weather_template = change_weather_value(
            type=f"RioDeJaneiroMareAltura{number}",
            city="",
            value=tide_table[index]["tide"],
            template=weather_template,
            first_letter_upper=True,
        )
        #     dataset.append(
        #         BeautifulSoup(
        #             f"<RioDeJaneiroMareAltura{number}><p>{tide_table[index]['tide']}</p>"
        #             + f"</RioDeJaneiroMareAltura{number}>",
        #             "xml",
        #         )
        #     )
        weather_template = change_weather_value(
            type=f"RioDeJaneiroMareHora{number}",
            city="",
            value=tide_table[index]["time"],
            template=weather_template,
            first_letter_upper=True,
        )
        #     dataset.append(
        #         BeautifulSoup(
        #             f"<RioDeJaneiroMareHora{number}><p>{tide_table[index]['time']}</p>"
        #             + f"</RioDeJaneiroMareHora{number}>",
        #             "xml",
        #         )
        #     )
        weather_template = change_weather_value(
            type=f"RioDeJaneiroMareIcone{number}",
            city="",
            value=icon,
            template=weather_template,
            first_letter_upper=True,
        )
    #     dataset.append(
    #         BeautifulSoup(
    #             f"<RioDeJaneiroMareIcone{number}>{icon}</RioDeJaneiroMareIcone{number}>",
    #             "xml",
    #         )
    #     )
    # weather_template.append(dataset)
    return weather_template


def build_map_template(weather: List[ForecastType], storage: IStorage):
    logger.info("Building map termplate")
    weather_template = open_weather_template()
    tide_table = json.loads(
        storage.get_file(file_path="climatempo/tide/tide-table.json").decode("utf-8")
    )
    for city_weather in weather:
        city_weather["data"] = city_weather["data"][1:]
        weather_template = temperature(city_weather, weather_template)
        weather_template = thermal_sensation(city_weather, weather_template)
        weather_template = rain_probability_icon(city_weather, weather_template)
        weather_template = sunrise_and_sunset_in_rj(city_weather, weather_template)
        weather_template = rain_probability_in_rj_week(city_weather, weather_template)
        weather_template = temperature_in_rj_zones(city_weather, weather_template)
        weather_template = max_and_min_temperature_in_rj(city_weather, weather_template)
    weather_template = moon_phases(weather_template)
    weather_template = rj_tide_table(tide_table, weather_template)
    save_completed_template(template=weather_template, storage=storage)
