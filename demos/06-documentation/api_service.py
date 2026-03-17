"""
Undocumented API Service — Documentation Generation Demo

This module implements an API client for a weather service.
It is intentionally written WITHOUT any docstrings or comments.

DEMO INSTRUCTIONS:
==================
1. Select the entire file and use Copilot Chat: /doc
2. Or select individual methods, right-click → Copilot → Generate Docs
3. Ask Copilot Chat: "Generate a README.md for this module"
4. Ask: "Generate an OpenAPI/Swagger spec for this service"
5. Ask: "Create a usage guide with examples for this module"
6. Show inline chat (Cmd+I): "Add docstrings to all methods in this class"
"""

import hashlib
import hmac
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional
from urllib.parse import urlencode


class Units(Enum):
    METRIC = "metric"
    IMPERIAL = "imperial"
    STANDARD = "standard"


class ApiError(Exception):
    def __init__(self, status_code: int, message: str, response_body: Optional[dict] = None):
        self.status_code = status_code
        self.message = message
        self.response_body = response_body
        super().__init__(f"[{status_code}] {message}")


@dataclass
class Location:
    latitude: float
    longitude: float
    city: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None

    def to_query_params(self) -> dict:
        if self.city:
            q = self.city
            if self.state:
                q += f",{self.state}"
            if self.country:
                q += f",{self.country}"
            return {"q": q}
        return {"lat": self.latitude, "lon": self.longitude}


@dataclass
class WeatherData:
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    wind_speed: float
    wind_direction: int
    description: str
    icon: str
    visibility: int
    clouds: int
    timestamp: int
    location: Location
    units: Units

    @property
    def temperature_formatted(self) -> str:
        suffix = {"metric": "°C", "imperial": "°F", "standard": "K"}
        return f"{self.temperature:.1f}{suffix[self.units.value]}"

    @property
    def wind_speed_formatted(self) -> str:
        suffix = {"metric": "m/s", "imperial": "mph", "standard": "m/s"}
        return f"{self.wind_speed:.1f} {suffix[self.units.value]}"


class WeatherApiClient:
    BASE_URL = "https://api.weatherservice.example.com/v2"
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3

    def __init__(self, api_key: str, secret_key: Optional[str] = None,
                 units: Units = Units.METRIC, timeout: int = DEFAULT_TIMEOUT):
        self._api_key = api_key
        self._secret_key = secret_key
        self._units = units
        self._timeout = timeout
        self._cache: dict[str, tuple[float, Any]] = {}
        self._cache_ttl = 300
        self._request_count = 0

    def _build_url(self, endpoint: str, params: Optional[dict] = None) -> str:
        url = f"{self.BASE_URL}/{endpoint}"
        query_params = {"appid": self._api_key, "units": self._units.value}
        if params:
            query_params.update(params)
        return f"{url}?{urlencode(query_params)}"

    def _sign_request(self, endpoint: str, timestamp: int) -> str:
        if not self._secret_key:
            return ""
        message = f"{endpoint}:{timestamp}:{self._api_key}"
        return hmac.new(
            self._secret_key.encode(),
            message.encode(),
            hashlib.sha256,
        ).hexdigest()

    def _get_cached(self, cache_key: str) -> Optional[Any]:
        if cache_key in self._cache:
            cached_time, cached_data = self._cache[cache_key]
            if time.time() - cached_time < self._cache_ttl:
                return cached_data
            del self._cache[cache_key]
        return None

    def _set_cache(self, cache_key: str, data: Any) -> None:
        self._cache[cache_key] = (time.time(), data)

    def get_current_weather(self, location: Location) -> WeatherData:
        params = location.to_query_params()
        cache_key = f"current:{urlencode(params)}"

        cached = self._get_cached(cache_key)
        if cached:
            return cached

        # In a real implementation, this would make an HTTP request
        # For demo purposes, we simulate the response parsing
        response = self._simulate_api_call("weather", params)
        weather = self._parse_weather_response(response, location)
        self._set_cache(cache_key, weather)
        return weather

    def get_forecast(self, location: Location, days: int = 5) -> list[WeatherData]:
        if not 1 <= days <= 16:
            raise ValueError("Forecast days must be between 1 and 16")

        params = {**location.to_query_params(), "cnt": days * 8}
        cache_key = f"forecast:{urlencode(params)}"

        cached = self._get_cached(cache_key)
        if cached:
            return cached

        response = self._simulate_api_call("forecast", params)
        forecasts = [
            self._parse_weather_response(item, location)
            for item in response.get("list", [])
        ]
        self._set_cache(cache_key, forecasts)
        return forecasts

    def get_air_quality(self, location: Location) -> dict:
        params = {"lat": location.latitude, "lon": location.longitude}
        response = self._simulate_api_call("air_pollution", params)
        return {
            "aqi": response.get("main", {}).get("aqi", 0),
            "components": response.get("components", {}),
            "timestamp": response.get("dt", 0),
        }

    def batch_weather(self, locations: list[Location]) -> dict[str, WeatherData]:
        results = {}
        for loc in locations:
            key = loc.city or f"{loc.latitude},{loc.longitude}"
            results[key] = self.get_current_weather(loc)
        return results

    def _parse_weather_response(self, data: dict, location: Location) -> WeatherData:
        main = data.get("main", {})
        wind = data.get("wind", {})
        weather_info = data.get("weather", [{}])[0]

        return WeatherData(
            temperature=main.get("temp", 0.0),
            feels_like=main.get("feels_like", 0.0),
            humidity=main.get("humidity", 0),
            pressure=main.get("pressure", 0),
            wind_speed=wind.get("speed", 0.0),
            wind_direction=wind.get("deg", 0),
            description=weather_info.get("description", ""),
            icon=weather_info.get("icon", ""),
            visibility=data.get("visibility", 0),
            clouds=data.get("clouds", {}).get("all", 0),
            timestamp=data.get("dt", 0),
            location=location,
            units=self._units,
        )

    def _simulate_api_call(self, endpoint: str, params: dict) -> dict:
        self._request_count += 1
        return {
            "main": {"temp": 22.5, "feels_like": 21.0, "humidity": 65, "pressure": 1013},
            "wind": {"speed": 3.5, "deg": 180},
            "weather": [{"description": "partly cloudy", "icon": "02d"}],
            "visibility": 10000,
            "clouds": {"all": 40},
            "dt": int(time.time()),
        }

    def clear_cache(self) -> int:
        count = len(self._cache)
        self._cache.clear()
        return count

    @property
    def request_count(self) -> int:
        return self._request_count
