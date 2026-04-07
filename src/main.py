from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router as api_router
from src.db.postgres import pg
from src.db.redis_client import redis_client

app = FastAPI(
    title="INFINITUM Game Master API",
    version="1.0.0",
    description="Core engine for the Infinite Open World project.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.on_event("startup")
async def on_startup():
    try:
        await pg.connect()
    except Exception:
        pass
    try:
        await redis_client.connect()
    except Exception:
        pass


@app.on_event("shutdown")
async def on_shutdown():
    try:
        await pg.close()
    except Exception:
        pass
    try:
        await redis_client.close()
    except Exception:
        pass


@app.get("/health")
async def health_check():
    return {"status": "ok"}
