"""
Weather Tool
Integrates with OpenWeatherMap API to fetch current weather data
"""

import requests
import os
from typing import Dict, Any, Optional
from .base_tool import BaseTool


class WeatherTool(BaseTool):
    """OpenWeatherMap API integration tool"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    @property
    def name(self) -> str:
        return "weather_fetch"
    
    @property
    def description(self) -> str:
        return "Get current weather information for any city. Returns temperature, conditions, humidity, wind speed, and description. Use this when user asks about weather or temperature in a location."
    
    def execute(self, city: str, units: str = "metric") -> Dict[str, Any]:
        """
        Fetch current weather for a city
        
        Args:
            city: City name
            units: Temperature units ('metric' for Celsius, 'imperial' for Fahrenheit)
            
        Returns:
            Dict with success status and weather data
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "OPENWEATHER_API_KEY not configured. Get free API key from https://openweathermap.org/api",
                "data": None
            }
        
        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units
            }
            
            response = requests.get(
                self.base_url,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                weather_data = {
                    "city": data.get("name"),
                    "country": data.get("sys", {}).get("country"),
                    "temperature": data.get("main", {}).get("temp"),
                    "feels_like": data.get("main", {}).get("feels_like"),
                    "humidity": data.get("main", {}).get("humidity"),
                    "description": data.get("weather", [{}])[0].get("description", ""),
                    "wind_speed": data.get("wind", {}).get("speed"),
                    "units": "°C" if units == "metric" else "°F"
                }
                
                return {
                    "success": True,
                    "data": weather_data
                }
            
            elif response.status_code == 401:
                return {
                    "success": False,
                    "error": "Invalid OpenWeatherMap API key",
                    "data": None
                }
            
            elif response.status_code == 404:
                return {
                    "success": False,
                    "error": f"City '{city}' not found",
                    "data": None
                }
            
            else:
                return {
                    "success": False,
                    "error": f"Weather API error: {response.status_code}",
                    "data": None
                }
        
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Weather API request timed out",
                "data": None
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Weather tool error: {str(e)}",
                "data": None
            }
