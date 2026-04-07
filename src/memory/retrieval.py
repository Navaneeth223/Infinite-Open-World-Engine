from typing import Any
from src.db.postgres import pg
from src.memory.embedder import embedder
from src.memory.vector_store import vector_store


class MemoryRetrieval:
    async def get_relevant_world_events(self, world_id: str, query_text: str, n_results: int = 5) -> list[dict[str, Any]]:
        embedding = await embedder.embed(query_text)
        result = await vector_store.query(
            collection=f"world_{world_id}_events",
            query_embeddings=[embedding],
            n_results=n_results,
            where={"resolved": False},
        )
        return [
            {"text": doc, **meta}
            for doc, meta in zip(result.get("documents", []), result.get("metadatas", []))
        ]

    async def get_npc_memories(self, npc_id: str, query_text: str, n_results: int = 3) -> list[dict[str, Any]]:
        embedding = await embedder.embed(query_text)
        result = await vector_store.query(
            collection=f"npc_{npc_id}_memories",
            query_embeddings=[embedding],
            n_results=n_results,
            where={"forgotten": False},
        )
        return [
            {"text": doc, **meta}
            for doc, meta in zip(result.get("documents", []), result.get("metadatas", []))
        ]

    async def build_context(self, player_id: str, player_input: str, location_id: str, world_id: str) -> dict[str, Any]:
        player = await pg.fetchrow("SELECT * FROM players WHERE id = $1", player_id)
        location = await pg.fetchrow("SELECT * FROM locations WHERE id = $1", location_id)
        npcs = await pg.fetch("SELECT * FROM npcs WHERE location_id = $1 AND is_dead = FALSE", location_id)
        recent_actions = await pg.fetch("SELECT action_text FROM player_actions WHERE player_id = $1 ORDER BY real_timestamp DESC LIMIT 5", player_id)

        context = {
            "session": {},
            "recent_actions": [row["action_text"] for row in recent_actions],
            "location": location or {},
            "npcs_present": npcs,
            "npc_memories": {},
            "relevant_events": await self.get_relevant_world_events(world_id, f"{player_input} | location: {location['name'] if location else 'unknown'}"),
            "active_quests": await pg.fetch("SELECT * FROM quests WHERE player_id = $1 AND status = 'active'", player_id),
            "player": player or {},
            "factions": await pg.fetch("SELECT * FROM factions WHERE world_id = $1", world_id),
        }

        for npc in npcs:
            memories = await self.get_npc_memories(npc["id"], f"player interaction | {player_input}")
            context["npc_memories"][npc["id"]] = memories

        return context


retrieval = MemoryRetrieval()
