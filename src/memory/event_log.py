from typing import Any
from src.db.postgres import pg


class EventLog:
    async def log_player_action(self, player_id: str, world_id: str, action_text: str, location_id: str | None = None, npcs_involved: list[str] | None = None) -> None:
        await pg.execute(
            """
            INSERT INTO player_actions (player_id, world_id, action_type, action_text, location_id, npcs_involved, game_date, real_timestamp, ai_response, consequence_events, morality_tags, embedding_id)
            VALUES ($1, $2, $3, $4, $5, $6, $7, NOW(), $8, $9, $10, $11)
            """,
            player_id,
            world_id,
            "custom",
            action_text,
            location_id,
            npcs_involved or [],
            {},
            "",
            [],
            [],
            None,
        )


event_log = EventLog()
