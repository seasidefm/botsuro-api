from typing import Union

import requests

class OpenWeatherApi:
    """
    API wrapper for connecting to OpenWeather
    """
    def __init__(self, api_key: str):
        self.base_url = f"https://api.openweathermap.org/data/3.0/onecall?lat=LATITUDE&lon=LONGITUDE" \
            "&appid={api_key}&exclude=minutely,alerts"

    def get_weather_for_coords(self, latitude: Union[str, float], longitude: Union[str, float]):
        """
        Get the weather for a given set of coordinates
        :param latitude:
        :param longitude:
        :return:
        """

        formatted_url = self.base_url.replace('LATITUDE', str(latitude)).replace('LONGITUDE', str(longitude))

        data = requests.get(formatted_url)

        return data.json()
