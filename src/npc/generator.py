import uuid
from typing import Any
from src.brain.prompts import build_system_prompt
from src.brain.story import generate_gm_response


class NPCGenerator:
    async def create_npc(self, world_name: str, world_lore: str, location_name: str, location_type: str, region_name: str, player_reputation: int) -> dict[str, Any]:
        npc_id = str(uuid.uuid4())
        personality = {
            "openness": 0.5,
            "conscientiousness": 0.5,
            "extraversion": 0.5,
            "agreeableness": 0.5,
            "neuroticism": 0.5,
        }
        return {
            "id": npc_id,
            "name": "Mira the Watcher",
            "age": 34,
            "gender": "female",
            "race": "Human",
            "profession": "keeper",
            "title": "Innkeeper",
            "physical_description": "A squat woman with a scar along her cheek and a permanent half-smile.",
            "life_history": "Born in the borderlands, she learned to keep secrets and keeps her own. She has survived three winters of war and three more winters of quiet. She prefers to listen before she speaks.",
            "secret": "She keeps letters from a lost lover hidden under her bed.",
            "desire": "To keep her tavern intact through the coming storm.",
            "fear": "Losing everyone who comes through her door.",
            "personality_summary": "Guarded but observant, she notices what visitors do not say.",
            "speaking_style": "Uses calm, measured sentences and chooses her words carefully.",
            "current_mood": "neutral",
            "current_activity": "tending the bar and watching the door.",
            "schedule": {
                "dawn": "prepares breakfast and checks supplies",
                "morning": "welcomes early customers",
                "afternoon": "listens to travelers' stories",
                "evening": "keeps the tavern under control",
                "night": "locks the back door and counts coins",
            },
            **personality,
            "wealth_level": 2,
            "initial_player_stance": "indifferent",
            "first_words": "'You look like you have a story worth hearing.'",
        }

npc_generator = NPCGenerator()
