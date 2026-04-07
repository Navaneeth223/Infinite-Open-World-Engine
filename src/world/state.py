from typing import Any
from src.db.postgres import pg


class WorldStateManager:
    @staticmethod
    async def get_world(world_id: str) -> dict | None:
        if not pg.is_connected:
            return None
        return await pg.fetchrow("SELECT * FROM worlds WHERE id = $1", world_id)

    @staticmethod
    async def get_location(location_id: str) -> dict | None:
        if not pg.is_connected:
            return None
        return await pg.fetchrow("SELECT * FROM locations WHERE id = $1", location_id)

    @staticmethod
    async def get_active_world_events(world_id: str) -> list[dict]:
        if not pg.is_connected:
            return []
        return await pg.fetch(
            "SELECT * FROM world_events WHERE world_id = $1 AND resolved = FALSE ORDER BY real_timestamp DESC LIMIT 10",
            world_id,
        )

    @staticmethod
    async def get_npcs_at_location(location_id: str) -> list[dict]:
        if not pg.is_connected:
            return []
        return await pg.fetch(
            "SELECT * FROM npcs WHERE location_id = $1 AND is_dead = FALSE",
            location_id,
        )

    @staticmethod
    async def get_player(player_id: str) -> dict | None:
        if not pg.is_connected:
            return None
        return await pg.fetchrow("SELECT * FROM players WHERE id = $1", player_id)

    @staticmethod
    async def get_player_journal(player_id: str) -> list[dict]:
        if not pg.is_connected:
            return []
        return await pg.fetch(
            "SELECT * FROM player_journal WHERE player_id = $1 ORDER BY real_timestamp DESC LIMIT 50",
            player_id,
        )

    @staticmethod
    async def get_npc_relationship(npc_id: str, player_id: str) -> dict | None:
        if not pg.is_connected:
            return None
        return await pg.fetchrow(
            "SELECT id, player_relationship_score, player_relationship_label, times_met, last_seen_game_date FROM npcs WHERE id = $1",
            npc_id,
        )

    @staticmethod
    async def get_world_map(world_id: str, discovered_only: bool = True) -> dict:
        if not pg.is_connected:
            return {}
        world = await pg.fetchrow("SELECT * FROM worlds WHERE id = $1", world_id)
        if world is None:
            return {}

        regions = await pg.fetch("SELECT * FROM regions WHERE world_id = $1", world_id)
        locations = await pg.fetch(
            "SELECT l.* FROM locations l JOIN regions r ON l.region_id = r.id WHERE r.world_id = $1" + (" AND l.is_discovered = TRUE" if discovered_only else ""),
            world_id,
        )
        return {
            "world_id": world_id,
            "world_name": world.get("name"),
            "regions": regions,
            "locations": locations,
        }

    @staticmethod
    async def create_world(world_data: dict) -> dict:
        if not pg.is_connected:
            return world_data
        query = """
            INSERT INTO worlds (id, name, seed, lore, calendar_system, current_date)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING *
        """
        row = await pg.fetchrow(
            query,
            world_data["id"],
            world_data["name"],
            world_data.get("seed", 0),
            world_data.get("lore", ""),
            world_data.get("calendar_system", {}),
            world_data.get("current_date", {}),
        )
        return row or world_data

    @staticmethod
    async def tick_world(world_id: str) -> dict:
        return {"world_id": world_id, "status": "ticked"}
