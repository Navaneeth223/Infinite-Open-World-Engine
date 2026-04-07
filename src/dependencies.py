from fastapi import Depends
from src.db.postgres import pg
from src.db.redis_client import redis_client


async def get_pg():
    await pg.connect()
    return pg


async def get_redis():
    await redis_client.connect()
    return redis_client
