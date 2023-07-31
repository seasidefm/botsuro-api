from typing import Union, List

from repositories.weather import OpenWeatherAPI


class WeatherService:
    """
    API wrapper for connecting to OpenWeather

    :class:`WeatherService` is a class that provides methods to retrieve weather information from the OpenWeather API.

    .. note::
        This class requires the `OpenWeatherAPI` class from the `repositories.weather` module.

    Attributes:
        openweather (OpenWeatherAPI): An instance of the `OpenWeatherAPI` class.

    Methods:
        get_weather_for_coords: Get the weather for a given set of coordinates.

    """

    def __init__(self):
        self.openweather = OpenWeatherAPI()

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

        return self.openweather.get_weather_for_coords(
            latitude=latitude, longitude=longitude, selected_data=selected_data
        )
