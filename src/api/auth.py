from fastapi import Header, HTTPException
from src.config import settings


async def get_api_key(x_api_key: str | None = Header(default=None)) -> str | None:
    if settings.api_secret_key is None:
        return None
    if x_api_key == settings.api_secret_key:
        return x_api_key
    raise HTTPException(status_code=401, detail="Invalid API key")
