import pytest
from src.brain.parser import parse_gm_response
from src.brain.prompts import build_system_prompt


def test_parse_valid_gm_response():
    valid_json = '''
    {
        "narration": "You enter the dimly lit tavern...",
        "scene_mood": "tense",
        "location_changed": false,
        "time_elapsed_minutes": 5,
        "consequences": [],
        "npcs_interacted": [],
        "quest_updates": []
    }
    '''
    result = parse_gm_response(valid_json)
    assert result["scene_mood"] == "tense"
    assert result["location_changed"] is False


def test_parse_handles_malformed_json():
    malformed = "Here is the story: {broken json"
    result = parse_gm_response(malformed)
    assert result is not None
    assert "narration" in result
    assert result["narration"] == malformed


def test_system_prompt_includes_required_fields():
    context = {
        "world_name": "Ashenveil",
        "game_date": "Year 342, Month 3, Day 12",
        "current_location_name": "Ruined Bastion",
        "current_location_description": "A shattered fortress overrun by weeds.",
        "current_weather": "misty rain",
        "time_of_day": "morning",
        "region_name": "Grey Marsh",
        "region_description": "A damp borderland where fog never lifts.",
        "player_name": "Asha",
        "player_race": "Human",
        "player_class": "Scholar",
        "player_level": 5,
        "player_health": 85,
        "player_max_health": 100,
        "player_gold": 12,
        "player_global_reputation": 10,
        "player_status_effects": "none",
        "recent_player_history": ["Talked to the gate guard."],
        "active_world_events": ["A merchant caravan vanished"],
        "npcs_present": ["Gate guard"],
        "retrieved_memories": ["You once helped a farmer."],
        "active_quests": ["Investigate the caravan"],
    }
    prompt = build_system_prompt(context)
    assert "ASHENVEIL" not in prompt  # ensure not placeholder text
    assert "PLAYER" in prompt
    assert "WORLD STATE" in prompt
