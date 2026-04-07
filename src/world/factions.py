from typing import Dict, Any
from src.db.postgres import pg


class FactionEngine:
    async def evaluate_tensions(self, world_id: str) -> None:
        relations = await pg.fetch(
            "SELECT * FROM faction_relations WHERE faction_a IN (SELECT id FROM factions WHERE world_id = $1)",
            world_id,
        )
        for relation in relations:
            pass

    def calculate_tension(self, faction_a: Dict[str, Any], faction_b: Dict[str, Any], relation: Dict[str, Any]) -> float:
        tension = 0.0
        if faction_a.get("ideology") and faction_b.get("ideology") and faction_a["ideology"] != faction_b["ideology"]:
            tension += 0.1
        tension += relation.get("strength", 0.5) * 0.2
        return min(1.0, tension)


faction_engine = FactionEngine()
