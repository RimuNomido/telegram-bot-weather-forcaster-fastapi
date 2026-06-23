from dataclasses import dataclass

@dataclass
class WeatherData:
    cloudiness: str
    humidity: int
    precType: str
    precStrength: str
    pressure: int
    temperature: int
    fahrenheit: int
    windSpeed: float
    windDirection: str

class WeatherParser:
    cloudiness_ru = {
        "CLEAR": "Ясно",
        "PARTLY": "Малооблачно",
        "SIGNIFICANT": "Переменная облачность",
        "CLOUDY": "Облачно",
        "OVERCAST": "Пасмурно"
    }
    cloudiness_emojis = {
        "CLEAR": "☀️",
        "PARTLY": "🌤️",
        "SIGNIFICANT": "🌥️",
        "CLOUDY": "⛅",
        "OVERCAST": "☁️"
    }

    prec_type_ru = {
        "NO_TYPE": "Нет осадков",
        "RAIN": "Дождь",
        "SLEET": "Дождь со снегом",
        "SNOW": "Снег",
        "HAIL": "Град"
    }
    prec_type_emojis = {
        "NO_TYPE": "🚫",
        "RAIN": "🌧️",
        "SLEET": "🌨️",
        "SNOW": "❄️",
        "HAIL": "⛈️"
    }

    prec_strength_ru = {
        "ZERO": "Отсутствует",
        "WEAK": "Слабая",
        "AVERAGE": "Умеренная",
        "STRONG": "Сильная",
        "VERY_STRONG": "Очень сильная"
    }
    prec_strength_emojis = {
        "ZERO": "🛑",
        "WEAK": "💧",
        "AVERAGE": "🌧️",
        "STRONG": "🚶‍♂️🌧️",
        "VERY_STRONG": "🌊"
    }

    wind_dir_ru = {
        "CALM": "Штиль",
        "NORTH": "Север",
        "NORTH_EAST": "Северо-восток",
        "EAST": "Восток",
        "SOUTH_EAST": "Юго-восток",
        "SOUTH": "Юг",
        "SOUTH_WEST": "Юго-запад",
        "WEST": "Запад",
        "NORTH_WEST": "Северо-запад"
    }
    wind_dir_emojis = {
        "CALM": "⚓",
        "NORTH": "⬆️",        # На север (вверх)
        "NORTH_EAST": "↗️",   # На северо-восток (вверх-вправо)
        "EAST": "➡️",         # На восток (вправо)
        "SOUTH_EAST": "↘️",   # На юго-восток (вниз-вправо)
        "SOUTH": "⬇️",        # На юг (вниз)
        "SOUTH_WEST": "↙️",   # На юго-запад (вниз-влево)
        "WEST": "⬅️",         # На запад (влево)
        "NORTH_WEST": "↖️"    # На северо-запад (вверх-влево)
    }


    @staticmethod
    def get_wind_speed_emoji(speed: float) -> str:
        if speed < 2.0:
            return "🍃"
        elif speed < 5.0:
            return "💨"
        elif speed < 10.0:
            return "🌬️"
        else:
            return "🌪️"

    @staticmethod
    def get_humidity_emoji(humidity: int) -> str:
        if humidity < 40:
            return "🏜️"
        elif humidity <= 70:
            return "💧"
        else:
            return "💦"

    static_emojis = {
        "date": "🗓️",
        "city": "📍",
        "pressure": "🧭",
        "temp_c": "🌡️",
        "temp_f": "🇺🇸"
    }


def parse_to_display(data: WeatherData, city: str) -> str:
    c_emoji = WeatherParser.cloudiness_emojis.get(data.cloudiness, "🌥️")
    c_text = WeatherParser.cloudiness_ru.get(data.cloudiness, data.cloudiness)

    pt_emoji = WeatherParser.prec_type_emojis.get(data.precType, "❓")
    pt_text = WeatherParser.prec_type_ru.get(data.precType, data.precType)

    ps_emoji = WeatherParser.prec_strength_emojis.get(data.precStrength, "📊")
    ps_text = WeatherParser.prec_strength_ru.get(data.precStrength, data.precStrength)

    wd_emoji = WeatherParser.wind_dir_emojis.get(data.windDirection, "🧭")
    wd_text = WeatherParser.wind_dir_ru.get(data.windDirection, data.windDirection)
    
    w_speed_emoji = WeatherParser.get_wind_speed_emoji(data.windSpeed)
    humidity_emoji = WeatherParser.get_humidity_emoji(data.humidity)
    
    se = WeatherParser.static_emojis

    return f"""
    {se['city']} Погода: {city}
    Облачность: {c_emoji} {c_text}
    Влажность: {humidity_emoji} {data.humidity}%
    Тип осадков: {pt_emoji} {pt_text}
    Интенсивность осадков: {ps_emoji} {ps_text}
    Атмосферное давление: {se['pressure']} {data.pressure} мм рт. ст.
    Температура: {se['temp_c']} {data.temperature} °C
    Температура по Фаренгейту: {se['temp_f']} {data.fahrenheit} °F
    Скорость ветра: {w_speed_emoji} {data.windSpeed} м/с
    Направление ветра: {wd_emoji} {wd_text}"""

def display_all_history(answers: list[str], count_displayed, count_all):
    consolidated_answer = 'ИСТОРИЯ ЗАПРОСОВ'.center(50, '=') + '\n'
    for i in range(count_displayed):
        answer = answers[i]
        if i == count_displayed - 1:
            consolidated_answer += answer + '\n'
            consolidated_answer += f'ОБЩЕЕ КОЛИЧЕСТВО ВСЕХ ЗАПРОСОВ: {count_all}'.center(50, '=')
            break
        consolidated_answer += answer + "\n" + '='*50 + '\n'
    return consolidated_answer

def parse_query_to_story(data, city, query_date):
    date_str = f'🗓️ Дата: {query_date}'
    parsed_weather_data = parse_to_display(data, city)
    parsed_query = date_str + parsed_weather_data
    return parsed_query

def parse_json(json) -> WeatherData:
    try:
        weather = json['data']['weatherByPoint']['now']
        return WeatherData(**weather)
    except (KeyError, TypeError):
        return None
