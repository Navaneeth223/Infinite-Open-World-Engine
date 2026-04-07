from typing import Dict, Any


async def generate_npc_dialogue(npc_profile: Dict[str, Any], player_message: str) -> Dict[str, Any]:
    return {
        "dialogue": f"{npc_profile.get('name', 'The NPC')} listens carefully and replies with interest.",
        "tone": "neutral",
        "body_language": "The NPC holds their gaze steadily.",
        "relationship_delta": 0,
        "secret_proximity": 0.1,
        "offers_quest": False,
        "quest_hint": None,
        "memory_update": "The NPC remembers the tone of the conversation.",
    }
