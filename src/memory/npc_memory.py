from typing import Any
from src.memory.vector_store import vector_store
from src.memory.embedder import embedder


class NPCMemoryStore:
    def __init__(self) -> None:
        self._store = vector_store

    async def store(self, npc_id: str, memory: str, emotional_weight: float, game_date: dict[str, Any]) -> None:
        embedding = await embedder.embed(memory)
        await self._store.add(
            collection=f"npc_{npc_id}_memories",
            documents=[memory],
            embeddings=[embedding],
            metadatas=[{
                "memory_type": "player_interaction",
                "emotional_weight": emotional_weight,
                "game_date": game_date,
                "forgotten": False,
            }],
        )

    async def retrieve(self, npc_id: str, query: str, n_results: int = 3) -> list[dict[str, Any]]:
        query_embedding = await embedder.embed(query)
        results = await self._store.query(
            collection=f"npc_{npc_id}_memories",
            query_embeddings=[query_embedding],
            n_results=n_results,
            where={"forgotten": False},
        )
        return [
            {"memory": doc, **meta}
            for doc, meta in zip(results.get("documents", []), results.get("metadatas", []))
        ]


npc_memory_store = NPCMemoryStore()
