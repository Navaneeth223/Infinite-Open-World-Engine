from datetime import datetime
from src.db.postgres import pg


class WorldEventManager:
    async def create_event(self, world_id: str, event_type: str, title: str, description: str, location_id: str | None = None, region_id: str | None = None, affected_factions: list[str] | None = None, caused_by_player: bool = False, game_date: dict | None = None) -> dict:
        row = await pg.fetchrow(
            """
            INSERT INTO world_events (world_id, event_type, title, description, location_id, region_id, affected_factions, caused_by_player, game_date, real_timestamp, resolved, consequences, metadata)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, FALSE, $11, $12)
            RETURNING *
            """,
            world_id,
            event_type,
            title,
            description,
            location_id,
            region_id,
            affected_factions or [],
            caused_by_player,
            game_date or {},
            datetime.utcnow(),
            [],
            {},
        )
        return row or {}

    async def resolve_event(self, event_id: str) -> None:
        await pg.execute("UPDATE world_events SET resolved = TRUE WHERE id = $1", event_id)


world_event_manager = WorldEventManager()
