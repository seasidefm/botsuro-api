import os
from typing import Union, List

import requests


class OpenWeatherAPI:
    def __init__(self):
        if owm_token := os.getenv("OPEN_WEATHER_MAP_TOKEN"):
            self.base_url = \
                f"https://api.openweathermap.org/data/3.0/onecall?lat=LATITUDE&lon=LONGITUDE&appid={owm_token}"
        else:
            raise EnvironmentError("OPEN_WEATHER_MAP_TOKEN not found in env")

        self.exclude_options = [
            "current",
            "minutely",
            "hourly",
            "daily",
            "alerts",
        ]

    def get_weather_for_coords(self,
                               latitude: Union[str, float],
                               longitude: Union[str, float],
                               selected_data: List[str]
                               ):
        """
        Get the weather for a given set of coordinates

        :param latitude: The latitude of the location
        :type latitude: Union[str, float]
        :param longitude: The longitude of the location
        :type longitude: Union[str, float]
        :param selected_data: The selected weather data to include
        :type selected_data: List[str]
        :return: The weather data for the given coordinates
        :rtype: dict
        """

        formatted_url = self.base_url.replace('LATITUDE', str(latitude)).replace('LONGITUDE', str(longitude))
        # Nothing is included by default with this setup, so
        formatted_url += f"&exclude={','.join(filter(lambda x: x not in selected_data, self.exclude_options))}"

        data = requests.get(formatted_url)

        return data.json()
