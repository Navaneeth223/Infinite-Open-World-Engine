from typing import Any
from src.db.postgres import pg


class PlayerProfileStore:
    async def get_player(self, player_id: str) -> dict[str, Any] | None:
        return await pg.fetchrow("SELECT * FROM players WHERE id = $1", player_id)

    async def create_player(self, player_data: dict[str, Any]) -> dict[str, Any]:
        query = """
            INSERT INTO players
            (id, world_id, character_name, character_race, character_class, character_backstory, level, experience, health, max_health, strength, dexterity, intelligence, charisma, wisdom, reputation, current_location_id, inventory, gold, skills, status_effects)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21)
            RETURNING *
        """
        row = await pg.fetchrow(
            query,
            player_data["id"],
            player_data["world_id"],
            player_data["character_name"],
            player_data["character_race"],
            player_data["character_class"],
            player_data.get("character_backstory", ""),
            player_data.get("level", 1),
            player_data.get("experience", 0),
            player_data.get("health", 100),
            player_data.get("max_health", 100),
            player_data.get("strength", 10),
            player_data.get("dexterity", 10),
            player_data.get("intelligence", 10),
            player_data.get("charisma", 10),
            player_data.get("wisdom", 10),
            player_data.get("reputation", {}),
            player_data.get("current_location_id"),
            player_data.get("inventory", {}),
            player_data.get("gold", 50),
            player_data.get("skills", {}),
            player_data.get("status_effects", {}),
        )
        return row or {}


player_profile = PlayerProfileStore()
