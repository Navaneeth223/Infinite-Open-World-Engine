from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    openai_api_key: str | None = None
    openai_model: str = "gpt-4o"
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-opus-4-5"
    llm_max_tokens: int = 1024
    llm_temperature: float = 0.8

    database_url: str = "postgresql://infinitum:password@localhost:5432/infinitum"
    redis_url: str = "redis://localhost:6379"
    chroma_host: str = "localhost"
    chroma_port: int = 8001
    chroma_persist_dir: str = "./data/chroma"
    embedding_provider: str = "local"
    api_secret_key: str = "secret-key"

    world_tick_interval_seconds: int = 300
    real_to_game_time_ratio: int = 60
    autonomous_event_chance: float = 0.15
    npc_memory_decay_days: int = 30
    max_context_memories: int = 10


settings = Settings()
