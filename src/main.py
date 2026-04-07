from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router as api_router
from src.db.postgres import pg
from src.db.redis_client import redis_client


SCHEMA_SQL = """
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS worlds (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    seed BIGINT NOT NULL,
    lore TEXT,
    calendar_system JSONB,
    "current_date" JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS regions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    world_id UUID REFERENCES worlds(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50),
    climate VARCHAR(50),
    description TEXT,
    danger_level INTEGER DEFAULT 1,
    discovered BOOLEAN DEFAULT FALSE,
    coordinates JSONB,
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS locations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    region_id UUID REFERENCES regions(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50),
    description TEXT,
    population INTEGER DEFAULT 0,
    is_discovered BOOLEAN DEFAULT FALSE,
    is_destroyed BOOLEAN DEFAULT FALSE,
    coordinates JSONB,
    services JSONB,
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS world_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    world_id UUID REFERENCES worlds(id),
    event_type VARCHAR(100) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    location_id UUID REFERENCES locations(id),
    region_id UUID REFERENCES regions(id),
    affected_factions UUID[],
    caused_by_player BOOLEAN DEFAULT FALSE,
    player_action_id UUID,
    game_date JSONB NOT NULL,
    real_timestamp TIMESTAMP DEFAULT NOW(),
    resolved BOOLEAN DEFAULT FALSE,
    consequences JSONB,
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS player_actions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id UUID NOT NULL,
    world_id UUID REFERENCES worlds(id),
    action_type VARCHAR(100),
    action_text TEXT NOT NULL,
    location_id UUID REFERENCES locations(id),
    npcs_involved UUID[],
    game_date JSONB,
    real_timestamp TIMESTAMP DEFAULT NOW(),
    ai_response TEXT,
    consequence_events UUID[],
    morality_tags TEXT[],
    embedding_id VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS npcs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    world_id UUID REFERENCES worlds(id),
    location_id UUID REFERENCES locations(id),
    name VARCHAR(100) NOT NULL,
    age INTEGER,
    gender VARCHAR(20),
    race VARCHAR(50),
    profession VARCHAR(100),
    title VARCHAR(100),
    openness FLOAT DEFAULT 0.5,
    conscientiousness FLOAT DEFAULT 0.5,
    extraversion FLOAT DEFAULT 0.5,
    agreeableness FLOAT DEFAULT 0.5,
    neuroticism FLOAT DEFAULT 0.5,
    life_history TEXT,
    secret TEXT,
    desire TEXT,
    fear TEXT,
    moral_alignment VARCHAR(50),
    health VARCHAR(20) DEFAULT 'healthy',
    mood VARCHAR(50) DEFAULT 'neutral',
    wealth_level INTEGER DEFAULT 3,
    current_activity VARCHAR(200),
    schedule JSONB,
    faction_id UUID,
    home_location_id UUID REFERENCES locations(id),
    relationship_count INTEGER DEFAULT 0,
    player_relationship_score INTEGER DEFAULT 0,
    player_relationship_label VARCHAR(50) DEFAULT 'stranger',
    times_met INTEGER DEFAULT 0,
    last_seen_game_date JSONB,
    is_generated BOOLEAN DEFAULT TRUE,
    is_unique BOOLEAN DEFAULT FALSE,
    is_dead BOOLEAN DEFAULT FALSE,
    killed_by VARCHAR(200),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS player_journal (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id UUID REFERENCES players(id),
    entry_type VARCHAR(50),
    title VARCHAR(200),
    content TEXT NOT NULL,
    game_date JSONB,
    real_timestamp TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS players (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    world_id UUID REFERENCES worlds(id),
    character_name VARCHAR(100) NOT NULL,
    character_race VARCHAR(50),
    character_class VARCHAR(50),
    character_backstory TEXT,
    level INTEGER DEFAULT 1,
    experience INTEGER DEFAULT 0,
    health INTEGER DEFAULT 100,
    max_health INTEGER DEFAULT 100,
    strength INTEGER DEFAULT 10,
    dexterity INTEGER DEFAULT 10,
    intelligence INTEGER DEFAULT 10,
    charisma INTEGER DEFAULT 10,
    wisdom INTEGER DEFAULT 10,
    reputation JSONB,
    known_secrets TEXT[],
    titles_earned TEXT[],
    current_location_id UUID REFERENCES locations(id),
    inventory JSONB,
    gold INTEGER DEFAULT 50,
    skills JSONB,
    status_effects JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    last_active TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS factions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    world_id UUID REFERENCES worlds(id),
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50),
    description TEXT,
    ideology TEXT,
    goals TEXT,
    methods TEXT,
    military_power INTEGER DEFAULT 5,
    economic_power INTEGER DEFAULT 5,
    political_power INTEGER DEFAULT 5,
    is_at_war BOOLEAN DEFAULT FALSE,
    war_targets UUID[],
    territory JSONB,
    player_standing INTEGER DEFAULT 0,
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS faction_relations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    faction_a UUID REFERENCES factions(id),
    faction_b UUID REFERENCES factions(id),
    relation_type VARCHAR(50),
    strength FLOAT DEFAULT 0.5,
    history TEXT,
    UNIQUE(faction_a, faction_b)
);

CREATE TABLE IF NOT EXISTS markets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID REFERENCES locations(id),
    item_type VARCHAR(100),
    base_price INTEGER,
    current_price INTEGER,
    supply_level FLOAT DEFAULT 1.0,
    demand_level FLOAT DEFAULT 1.0,
    last_updated TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS weather_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    region_id UUID REFERENCES regions(id),
    weather_type VARCHAR(50),
    intensity FLOAT,
    game_date JSONB,
    duration_days INTEGER,
    effects JSONB
);

CREATE TABLE IF NOT EXISTS npc_memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    npc_id UUID REFERENCES npcs(id) ON DELETE CASCADE,
    memory_type VARCHAR(50),
    summary TEXT NOT NULL,
    full_detail TEXT,
    emotional_weight FLOAT DEFAULT 0.5,
    game_date JSONB,
    real_timestamp TIMESTAMP DEFAULT NOW(),
    is_forgotten BOOLEAN DEFAULT FALSE,
    embedding_id VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS npc_relationships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    npc_id UUID REFERENCES npcs(id),
    other_npc_id UUID REFERENCES npcs(id),
    relationship_type VARCHAR(50),
    strength FLOAT DEFAULT 0.5,
    history TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(npc_id, other_npc_id)
);

CREATE TABLE IF NOT EXISTS quests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    world_id UUID REFERENCES worlds(id),
    player_id UUID REFERENCES players(id),
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    quest_type VARCHAR(50),
    giver_npc_id UUID REFERENCES npcs(id),
    target_location_id UUID REFERENCES locations(id),
    objectives JSONB,
    failure_conditions JSONB,
    time_limit_game_days INTEGER,
    status VARCHAR(20) DEFAULT 'active',
    outcome_chosen VARCHAR(200),
    consequences_applied JSONB,
    reward_gold INTEGER DEFAULT 0,
    reward_items JSONB,
    reward_reputation JSONB,
    reward_experience INTEGER DEFAULT 0,
    generated_from_context TEXT,
    difficulty INTEGER DEFAULT 3,
    moral_complexity INTEGER DEFAULT 3,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_player_actions_player ON player_actions(player_id);
CREATE INDEX IF NOT EXISTS idx_player_actions_timestamp ON player_actions(real_timestamp);
CREATE INDEX IF NOT EXISTS idx_npc_memories_npc ON npc_memories(npc_id);
CREATE INDEX IF NOT EXISTS idx_world_events_world ON world_events(world_id);
CREATE INDEX IF NOT EXISTS idx_npcs_location ON npcs(location_id);
CREATE INDEX IF NOT EXISTS idx_quests_player ON quests(player_id);
CREATE INDEX IF NOT EXISTS idx_quests_status ON quests(status);
"""


async def _initialize_database() -> None:
    """Initialize database schema if not already created."""
    if not pg.is_connected or pg.pool is None:
        return
    try:
        # Split SQL statements by semicolon and execute each one individually
        statements = [stmt.strip() for stmt in SCHEMA_SQL.split(';') if stmt.strip()]
        conn = await pg.pool.acquire()
        try:
            for stmt in statements:
                await conn.execute(stmt)
        finally:
            await pg.pool.release(conn)
        print("INFO: Database tables created successfully")
    except Exception as e:
        print(f"WARNING: Database schema initialization encountered an issue: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await pg.connect()
        await _initialize_database()
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
