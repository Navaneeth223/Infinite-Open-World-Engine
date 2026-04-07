from typing import Any


class BrainRouter:
    async def route_action(self, payload: dict[str, Any]) -> dict[str, Any]:
        return payload

    async def route_npc(self, payload: dict[str, Any]) -> dict[str, Any]:
        return payload

    async def route_quest(self, payload: dict[str, Any]) -> dict[str, Any]:
        return payload

    async def route_world(self, payload: dict[str, Any]) -> dict[str, Any]:
        return payload


brain_router = BrainRouter()
