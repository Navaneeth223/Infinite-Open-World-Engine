from typing import Dict


def build_world_map(world: Dict, discovered_only: bool = True) -> Dict:
    return {
        "world_id": world.get("id"),
        "name": world.get("name"),
        "regions": world.get("regions", []),
        "locations": [loc for loc in world.get("locations", []) if not discovered_only or loc.get("is_discovered", False)],
    }
