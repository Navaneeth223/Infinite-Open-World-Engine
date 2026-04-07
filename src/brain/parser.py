import json
import re
from typing import Any


def _normalize_response(data: dict) -> dict:
    defaults = {
        "narration": "The world holds its breath for a moment.",
        "scene_mood": "mysterious",
        "location_changed": False,
        "new_location_id": None,
        "time_elapsed_minutes": 10,
        "consequences": [],
        "npcs_interacted": [],
        "quest_updates": [],
        "world_events_triggered": [],
        "suggested_music_mood": "mysterious",
        "ambient_sounds": [],
    }
    normalized = {**defaults, **{k: data.get(k, defaults[k]) for k in defaults}}
    return normalized


def _extract_json(text: str) -> str | None:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    return text[start:end + 1]


def parse_gm_response(raw_text: str) -> dict:
    if not raw_text or not raw_text.strip():
        return _normalize_response({
            "narration": "The world is quiet, waiting for your next move.",
        })

    try:
        parsed = json.loads(raw_text)
        return _normalize_response(parsed)
    except json.JSONDecodeError:
        extracted = _extract_json(raw_text)
        if extracted:
            try:
                parsed = json.loads(extracted)
                return _normalize_response(parsed)
            except json.JSONDecodeError:
                pass

    return _normalize_response({
        "narration": raw_text.strip(),
        "scene_mood": "mysterious",
        "consequences": [],
        "npcs_interacted": [],
        "quest_updates": [],
        "world_events_triggered": [],
    })
