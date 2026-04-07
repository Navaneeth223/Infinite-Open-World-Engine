from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router as api_router
from src.db.postgres import pg
from src.db.redis_client import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await pg.connect()
    except Exception:
        pass
    try:
        await redis_client.connect()
    except Exception:
        pass
    yield
    try:
        await pg.close()
    except Exception:
        pass
    try:
        await redis_client.close()
    except Exception:
        pass


app = FastAPI(
    title="INFINITUM Game Master API",
    version="1.0.0",
    description="Core engine for the Infinite Open World project.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
