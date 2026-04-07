from typing import Dict, Any


class WeatherEngine:
    async def update_weather(self, world_id: str) -> None:
        return

    def generate_weather(self, region: Dict[str, Any]) -> Dict[str, Any]:
        return {"weather_type": "cool drizzle", "intensity": 0.4, "effects": {"travel_speed": 0.9}}


weather_engine = WeatherEngine()
