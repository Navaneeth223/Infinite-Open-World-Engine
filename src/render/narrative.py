from typing import Dict


def format_narration(response: Dict) -> Dict:
    return {
        "narration": response.get("narration", ""),
        "scene_mood": response.get("scene_mood", "mysterious"),
        "suggested_music_mood": response.get("suggested_music_mood", "mysterious"),
        "ambient_sounds": response.get("ambient_sounds", []),
    }
