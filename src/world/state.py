import uuid
from typing import Any
from src.db.postgres import pg
from src.world.clock import WorldClock
from src.world.economy import economy_engine
from src.world.weather import weather_engine


class WorldStateManager:
    _world_store: dict[str, dict] = {}
    _player_store: dict[str, dict] = {}
    _journal_store: dict[str, list[dict]] = {}
    _event_store: dict[str, list[dict]] = {}
    _map_store: dict[str, dict] = {}

    @classmethod
    def _store_world(cls, world_data: dict) -> None:
        world_id = world_data["id"]
        starting_location = world_data.get("starting_location", {})
        region_id = f"{world_id}-region"
        location_id = starting_location.get("id") or f"{world_id}-location"

        starting_location = {
            **starting_location,
            "id": location_id,
            "region_id": region_id,
            "is_discovered": True,
        }
        world_data["starting_location"] = starting_location

        cls._world_store[world_id] = world_data
        cls._event_store[world_id] = world_data.get("initial_world_events", [])
        cls._map_store[world_id] = {
            "world_id": world_id,
            "world_name": world_data.get("name"),
            "regions": [
                {
                    "id": region_id,
                    "name": "Ashen Crossing",
                    "description": "A fringe borderland of ash-swept plains and battered stone ruins.",
                }
            ],
            "locations": [starting_location],
        }

    @classmethod
    async def create_player(cls, player_data: dict) -> dict:
        if pg.is_connected:
            query = """
                INSERT INTO players
                (id, world_id, character_name, character_race, character_class, character_backstory, level, experience, health, max_health, reputation, current_location_id, inventory, gold, status_effects)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
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
                player_data.get("reputation", {}),
                player_data.get("current_location_id"),
                player_data.get("inventory", {}),
                player_data.get("gold", 50),
                player_data.get("status_effects", {}),
            )
            return row or player_data

        cls._player_store[player_data["id"]] = player_data
        return player_data

    @staticmethod
    async def get_world(world_id: str) -> dict | None:
        if pg.is_connected:
            return await pg.fetchrow("SELECT * FROM worlds WHERE id = $1", world_id)
        return WorldStateManager._world_store.get(world_id)

    @staticmethod
    async def get_location(location_id: str) -> dict | None:
        if pg.is_connected:
            return await pg.fetchrow("SELECT * FROM locations WHERE id = $1", location_id)

        for world_map in WorldStateManager._map_store.values():
            for location in world_map.get("locations", []):
                if location.get("id") == location_id:
                    return location
        return None

    @staticmethod
    async def get_active_world_events(world_id: str) -> list[dict]:
        if pg.is_connected:
            return await pg.fetch(
                "SELECT * FROM world_events WHERE world_id = $1 AND resolved = FALSE ORDER BY real_timestamp DESC LIMIT 10",
                world_id,
            )
        return WorldStateManager._event_store.get(world_id, [])

    @staticmethod
    async def get_npcs_at_location(location_id: str) -> list[dict]:
        if pg.is_connected:
            return await pg.fetch(
                "SELECT * FROM npcs WHERE location_id = $1 AND is_dead = FALSE",
                location_id,
            )
        return []

    @staticmethod
    async def get_player(player_id: str) -> dict | None:
        if pg.is_connected:
            return await pg.fetchrow("SELECT * FROM players WHERE id = $1", player_id)
        return WorldStateManager._player_store.get(player_id)

    @staticmethod
    async def get_player_journal(player_id: str) -> list[dict]:
        if pg.is_connected:
            return await pg.fetch(
                "SELECT * FROM player_journal WHERE player_id = $1 ORDER BY real_timestamp DESC LIMIT 50",
                player_id,
            )
        return WorldStateManager._journal_store.get(player_id, [])

    @staticmethod
    async def get_npc_relationship(npc_id: str, player_id: str) -> dict | None:
        if pg.is_connected:
            return await pg.fetchrow(
                "SELECT id, player_relationship_score, player_relationship_label, times_met, last_seen_game_date FROM npcs WHERE id = $1",
                npc_id,
            )
        return None

    @staticmethod
    async def get_world_map(world_id: str, discovered_only: bool = True) -> dict:
        if pg.is_connected:
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

        world_map = WorldStateManager._map_store.get(world_id, {})
        if not world_map:
            return {}
        locations = [loc for loc in world_map.get("locations", []) if not discovered_only or loc.get("is_discovered", False)]
        return {
            "world_id": world_map["world_id"],
            "world_name": world_map["world_name"],
            "regions": world_map.get("regions", []),
            "locations": locations,
        }

    @staticmethod
    async def create_world(world_data: dict) -> dict:
        if pg.is_connected:
            query = """
                INSERT INTO worlds (id, name, seed, lore, calendar_system, "current_date")
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

        WorldStateManager._store_world(world_data)
        return world_data

    @staticmethod
    async def tick_world(world_id: str) -> dict:
        world = await WorldStateManager.get_world(world_id)
        if world is None:
            return {"world_id": world_id, "status": "ticked", "note": "world state unavailable"}

        current_date = world.get("current_date", {"year": 1, "month": 1, "day": 1, "hour": 9})
        next_hour = current_date.get("hour", 9) + 1
        next_day = current_date.get("day", 1)
        next_year = current_date.get("year", 1)

        if next_hour >= 24:
            next_hour = 0
            next_day += 1

        world["current_date"] = {
            "year": next_year,
            "month": current_date.get("month", 1),
            "day": next_day,
            "hour": next_hour,
        }

        await weather_engine.update_weather(world_id)
        await economy_engine.update_market(world_id)

        return {
            "world_id": world_id,
            "status": "ticked",
            "new_game_date": world["current_date"],
            "location_updates": world.get("starting_location", {}),
        }
