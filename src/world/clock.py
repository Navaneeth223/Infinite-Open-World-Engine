from dataclasses import dataclass


@dataclass
class WorldClock:
    world_id: str
    speed_multiplier: float = 1.0

    def game_time_from_real(self, real_seconds: float) -> dict:
        game_minutes = real_seconds * self.speed_multiplier
        total_game_hours = game_minutes / 60
        day = int(total_game_hours // 24) + 1
        hour = int(total_game_hours % 24)
        minute = int((total_game_hours - int(total_game_hours)) * 60)
        return {
            "day": day,
            "hour": hour,
            "minute": minute,
            "time_of_day": self.time_of_day(hour),
        }

    def time_of_day(self, game_hour: int) -> str:
        if 5 <= game_hour < 7:
            return "dawn"
        if 7 <= game_hour < 12:
            return "morning"
        if 12 <= game_hour < 14:
            return "midday"
        if 14 <= game_hour < 18:
            return "afternoon"
        if 18 <= game_hour < 21:
            return "evening"
        if 21 <= game_hour < 23:
            return "night"
        return "deep night"
