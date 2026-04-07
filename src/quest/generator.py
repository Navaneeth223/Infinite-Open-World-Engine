from typing import Dict, Any


class QuestGenerator:
    async def generate_emergent_quest(self, world_context: Dict[str, Any], player_context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "title": "A Rumor of a Missing Caravan",
            "description": "The roads are unsafe and a caravan has vanished. Someone needs to find out what happened before the region slips into chaos.",
            "quest_type": "emergent",
            "objectives": [
                {"id": "obj_1", "description": "Inspect the last known caravan route.", "type": "primary", "completion_condition": "report back with evidence"},
                {"id": "obj_2", "description": "Ask three travelers what they saw.", "type": "secondary", "completion_condition": "collect at least three accounts"},
            ],
            "failure_conditions": ["Arrive too late", "Ignore the caravan's trail"],
            "time_limit_game_days": 3,
            "difficulty": 3,
            "moral_complexity": 4,
            "rewards": {
                "gold": 50,
                "experience": 100,
                "items": [],
                "reputation_changes": [],
                "unique_reward": null,
            },
            "hidden_layer": "The caravan carried more than goods; it carried a secret message for the player's lost mentor.",
        }


quest_generator = QuestGenerator()
