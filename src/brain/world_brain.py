from typing import Dict, Any


async def generate_world_event(world_state_summary: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "event_type": "rumor_spreads",
        "title": "A rumor stirs unrest",
        "description": "A whispered story moves through the region and shifts the mood of the markets.",
        "affected_regions": [],
        "affected_factions": [],
        "affected_locations": [],
        "player_discovers_via": "rumor",
        "discovery_description": "You overhear the news in the tavern.",
        "immediate_effects": [],
        "delayed_effects": [],
        "player_opportunity": "Investigate the rumor",
        "reversible": True,
        "severity": 4,
    }
