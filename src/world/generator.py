import uuid
from typing import Any
from src.brain.story import generate_gm_response


class WorldGenerator:
    async def generate_seed_world(self, character_name: str, character_race: str, character_class: str, character_backstory: str) -> dict[str, Any]:
        world_id = str(uuid.uuid4())
        return {
            "id": world_id,
            "name": "Asterian Drift",
            "seed": 123456,
            "lore": "A land once shattered by celestial storms now clings to survival around fractured cities and scattered oases.",
            "calendar_system": {"year_length_days": 360, "months": ["Bram", "Lorn", "Hale", "Mist"], "era_name": "The Shattering", "current_year": 1},
            "game_date": {"year": 1, "month": 1, "day": 1, "hour": 9},
            "starting_location": {
                "name": "The Rusted Anvil Tavern",
                "type": "small_town",
                "description": "A cramped, iron-walled room filled with salt-sweet smoke and travelers who have nowhere else to go.",
                "atmosphere": "raw and watchful",
                "current_situation": "A journeyman has just arrived with a rumor of a collapsed trade route.",
                "population": 52,
                "notable_places": ["The Rusted Anvil", "Pearl Street Market", "Old Watchtower"]
            },
            "initial_world_events": [
                {"title": "Caravan vanishes on the western pass", "description": "A supply caravan failed to arrive, leaving merchants uneasy and guards restless.", "severity": 5, "affects": "local trade"}
            ],
            "main_quest_hook": {
                "title": "Echoes of a Lost Mentor",
                "connection_to_backstory": f"Your search for the truth behind your mentor's disappearance begins with rumors in the tavern.",
                "opening_clue": "A tattered letter addressed to you is found folded under the inn's hearthstone.",
                "ultimate_truth": "Your mentor was part of a secret order that shattered the world and hides in plain sight."
            }
        }

world_generator = WorldGenerator()
