from typing import Union, List

import requests


class OpenWeatherApi:
    """
    API wrapper for connecting to OpenWeather
    """

    def __init__(self, api_key: str):
        self.exclude_options = [
            "current",
            "minutely",
            "hourly",
            "daily",
            "alerts",
        ]

        self.base_url = \
            f"https://api.openweathermap.org/data/3.0/onecall?lat=LATITUDE&lon=LONGITUDE&appid={api_key}"

    def get_weather_for_coords(self,
                               latitude: Union[str, float],
                               longitude: Union[str, float],
                               selected_data: List[str]
                               ):
        """
        Get the weather for a given set of coordinates
        :param latitude:
        :param longitude:
        :param selected_data:
        :return:
        """

        formatted_url = self.base_url.replace('LATITUDE', str(latitude)).replace('LONGITUDE', str(longitude))
        # Nothing is included by default with this setup, so
        formatted_url += f"&exclude={','.join(filter(lambda x: x not in selected_data, self.exclude_options))}"

        data = requests.get(formatted_url)

        return data.json()
