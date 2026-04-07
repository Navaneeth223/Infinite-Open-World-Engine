import redis.asyncio as redis
from src.config import settings


class RedisClient:
    def __init__(self) -> None:
        self.client: redis.Redis | None = None

    async def connect(self) -> None:
        if self.client is None:
            self.client = redis.from_url(settings.redis_url, decode_responses=True)
            await self.client.ping()

    async def close(self) -> None:
        if self.client is not None:
            await self.client.close()
            self.client = None


redis_client = RedisClient()
