from __future__ import annotations

from typing import List

from pydantic import BaseModel


class WeatherItem(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class Current(BaseModel):
    dt: int
    sunrise: int
    sunset: int
    temp: float
    feels_like: float
    pressure: int
    humidity: int
    dew_point: float
    uvi: float
    clouds: int
    visibility: int
    wind_speed: float
    wind_deg: int
    wind_gust: float
    weather: List[WeatherItem]


class MinutelyItem(BaseModel):
    dt: int
    precipitation: int


class WeatherItem1(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class HourlyItem(BaseModel):
    dt: int
    temp: float
    feels_like: float
    pressure: int
    humidity: int
    dew_point: float
    uvi: float
    clouds: int
    visibility: int
    wind_speed: float
    wind_deg: int
    wind_gust: float
    weather: List[WeatherItem1]
    pop: int


class Temp(BaseModel):
    day: float
    min: float
    max: float
    night: float
    eve: float
    morn: float


class FeelsLike(BaseModel):
    day: float
    night: float
    eve: float
    morn: float


class WeatherItem2(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class DailyItem(BaseModel):
    dt: int
    sunrise: int
    sunset: int
    moonrise: int
    moonset: int
    moon_phase: float
    summary: str
    temp: Temp
    feels_like: FeelsLike
    pressure: int
    humidity: int
    dew_point: float
    wind_speed: float
    wind_deg: int
    wind_gust: float
    weather: List[WeatherItem2]
    clouds: int
    pop: int
    uvi: float


class WeatherData(BaseModel):
    lat: float
    lon: float
    timezone: str
    timezone_offset: int
    current: Current
    minutely: List[MinutelyItem]
    hourly: List[HourlyItem]
    daily: List[DailyItem]


class WeatherModel(BaseModel):
    data: WeatherData
