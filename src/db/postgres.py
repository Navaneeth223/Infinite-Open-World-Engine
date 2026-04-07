import asyncpg
from typing import Any
from src.config import settings


class Postgres:
    def __init__(self) -> None:
        self.pool: asyncpg.Pool | None = None

    @property
    def is_connected(self) -> bool:
        return self.pool is not None

    async def connect(self) -> None:
        if self.pool is None:
            self.pool = await asyncpg.create_pool(settings.database_url)

    async def close(self) -> None:
        if self.pool is not None:
            await self.pool.close()
            self.pool = None

    async def fetchrow(self, query: str, *args: Any) -> dict | None:
        if self.pool is None:
            raise RuntimeError("Postgres pool is not initialized")
        row = await self.pool.fetchrow(query, *args)
        return dict(row) if row is not None else None

    async def fetch(self, query: str, *args: Any) -> list[dict]:
        if self.pool is None:
            raise RuntimeError("Postgres pool is not initialized")
        rows = await self.pool.fetch(query, *args)
        return [dict(r) for r in rows]

    async def execute(self, query: str, *args: Any) -> None:
        if self.pool is None:
            raise RuntimeError("Postgres pool is not initialized")
        await self.pool.execute(query, *args)


pg = Postgres()
