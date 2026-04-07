from typing import Dict


def build_ui_state(world: Dict, player: Dict, npcs: list[Dict]) -> Dict:
    return {
        "world": {
            "id": world.get("id"),
            "name": world.get("name"),
            "current_date": world.get("game_date"),
        },
        "player": {
            "id": player.get("id"),
            "name": player.get("character_name"),
            "location_id": player.get("current_location_id"),
            "health": player.get("health"),
            "gold": player.get("gold"),
        },
        "npcs": npcs,
    }
