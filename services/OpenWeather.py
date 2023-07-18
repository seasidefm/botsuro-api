from typing import Union

import requests

from models.weather import WeatherModel, WeatherData


class OpenWeatherApi:
    def __init__(self, api_key: str):
        self.base_url = f"https://api.openweathermap.org/data/3.0/onecall?lat=LATITUDE&lon=LONGITUDE&appid={api_key}"

    def get_weather_for_coords(self, latitude: Union[str, float], longitude: Union[str, float]):
        formatted_url = self.base_url.replace('LATITUDE', str(latitude)).replace('LONGITUDE', str(longitude))

        data = requests.get(formatted_url)

        return data.json()
