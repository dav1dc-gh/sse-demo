

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
    """Client for interacting with the Weather Service API (v2).

    Provides methods to retrieve current weather, forecasts, and air quality
    data for one or more locations. Responses are cached in memory to reduce
    redundant API calls.

    Attributes:
        BASE_URL: The base URL for all API requests.
        DEFAULT_TIMEOUT: Default request timeout in seconds.
        MAX_RETRIES: Maximum number of retry attempts for failed requests.
    """

    BASE_URL = "https://api.weatherservice.example.com/v2"
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3

    def __init__(self, api_key: str, secret_key: Optional[str] = None,
                 units: Units = Units.METRIC, timeout: int = DEFAULT_TIMEOUT):
        """Initialize the weather API client.

        Args:
            api_key: Your API key for authentication.
            secret_key: Optional secret key used to sign requests via HMAC-SHA256.
            units: Unit system for temperature and wind speed. Defaults to metric.
            timeout: Request timeout in seconds. Defaults to 30.
        """
        self._api_key = api_key
        self._secret_key = secret_key
        self._units = units
        self._timeout = timeout
        self._cache: dict[str, tuple[float, Any]] = {}
        self._cache_ttl = 300
        self._request_count = 0

    def _build_url(self, endpoint: str, params: Optional[dict] = None) -> str:
        """Construct a full API URL with query parameters.

        Args:
            endpoint: The API endpoint path (e.g. "weather", "forecast").
            params: Additional query parameters to include.

        Returns:
            The fully qualified URL with encoded query string.
        """
        url = f"{self.BASE_URL}/{endpoint}"
        query_params = {"appid": self._api_key, "units": self._units.value}
        if params:
            query_params.update(params)
        return f"{url}?{urlencode(query_params)}"

    def _sign_request(self, endpoint: str, timestamp: int) -> str:
        """Generate an HMAC-SHA256 signature for a request.

        The signature is computed over the string ``endpoint:timestamp:api_key``
        using the secret key. If no secret key is configured, returns an empty string.

        Args:
            endpoint: The API endpoint being called.
            timestamp: Unix timestamp of the request.

        Returns:
            Hex-encoded HMAC signature, or an empty string if signing is disabled.
        """
        if not self._secret_key:
            return ""
        message = f"{endpoint}:{timestamp}:{self._api_key}"
        return hmac.new(
            self._secret_key.encode(),
            message.encode(),
            hashlib.sha256,
        ).hexdigest()

    def _get_cached(self, cache_key: str) -> Optional[Any]:
        """Retrieve a value from the in-memory cache if it has not expired.

        Expired entries are automatically removed.

        Args:
            cache_key: The unique key identifying the cached data.

        Returns:
            The cached data, or None if the key is missing or expired.
        """
        if cache_key in self._cache:
            cached_time, cached_data = self._cache[cache_key]
            if time.time() - cached_time < self._cache_ttl:
                return cached_data
            del self._cache[cache_key]
        return None

    def _set_cache(self, cache_key: str, data: Any) -> None:
        """Store a value in the in-memory cache with the current timestamp.

        Args:
            cache_key: The unique key to store the data under.
            data: The data to cache.
        """
        self._cache[cache_key] = (time.time(), data)

    def get_current_weather(self, location: Location) -> WeatherData:
        """Fetch current weather conditions for a location.

        Results are cached for the duration of the cache TTL (default 300 s).

        Args:
            location: The location to query weather for.

        Returns:
            A WeatherData object with the current conditions.
        """
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
        """Fetch a multi-day weather forecast for a location.

        The API returns data in 3-hour intervals, so the number of entries
        returned is ``days * 8``.

        Args:
            location: The location to query the forecast for.
            days: Number of forecast days (1–16). Defaults to 5.

        Returns:
            A list of WeatherData objects representing the forecast.

        Raises:
            ValueError: If days is not between 1 and 16.
        """
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
        """Fetch air quality data for a location.

        Args:
            location: The location to query. Latitude and longitude are required.

        Returns:
            A dict with keys ``aqi`` (Air Quality Index, 1–5),
            ``components`` (pollutant concentrations), and ``timestamp``.
        """
        params = {"lat": location.latitude, "lon": location.longitude}
        response = self._simulate_api_call("air_pollution", params)
        return {
            "aqi": response.get("main", {}).get("aqi", 0),
            "components": response.get("components", {}),
            "timestamp": response.get("dt", 0),
        }

    def batch_weather(self, locations: list[Location]) -> dict[str, WeatherData]:
        """Fetch current weather for multiple locations at once.

        Each location is queried individually via ``get_current_weather``.
        Results are keyed by city name or "latitude,longitude" if no city is set.

        Args:
            locations: The list of locations to query.

        Returns:
            A dict mapping location identifiers to their current WeatherData.
        """
        results = {}
        for loc in locations:
            key = loc.city or f"{loc.latitude},{loc.longitude}"
            results[key] = self.get_current_weather(loc)
        return results

    def _parse_weather_response(self, data: dict, location: Location) -> WeatherData:
        """Parse a raw API response dict into a WeatherData object.

        Args:
            data: The raw JSON response from the API.
            location: The location associated with this response.

        Returns:
            A populated WeatherData instance.
        """
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
        """Return a hardcoded response simulating an API call.

        This is a placeholder used for demo/testing purposes. In a real
        implementation it would perform an HTTP request to the weather service.

        Args:
            endpoint: The API endpoint to call.
            params: Query parameters for the request.

        Returns:
            A dict mimicking the structure of a real API response.
        """
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
        """Clear all cached responses.

        Returns:
            The number of entries that were removed.
        """
        count = len(self._cache)
        self._cache.clear()
        return count

    @property
    def request_count(self) -> int:
        """The total number of API calls made by this client instance."""
        return self._request_count
