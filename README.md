# INFINITUM Phase 1

Minimal core loop for the Infinite Open World Engine.

## Run locally

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Start the API:

```bash
uvicorn src.main:app --reload
```

3. Call the action endpoint:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/action \
  -H "Content-Type: application/json" \
  -H "x-api-key: secret-key" \
  -d '{"player_id":"player-1","world_id":"world-1","action_text":"I look around the tavern.","action_type":"examine"}'
```

> Note: API routes require the `x-api-key` header when `API_SECRET_KEY` is configured.

## Docker

Use Docker Compose to run the API with PostgreSQL, Redis, and ChromaDB:

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`.

## Testing

Install dev dependencies and run the test suite with:

```bash
python -m pip install -r requirements.txt
python -m pytest
```

## Notes

- API routes other than `/health` require the `x-api-key` header when `API_SECRET_KEY` is configured.

4. Initialize the database schema before using DB-backed endpoints:

```bash
python scripts/setup_db.py
```

5. Create a world:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/world/create \
  -H "Content-Type: application/json" \
  -d '{"character_name":"Asha","character_race":"Human","character_class":"Scholar","character_backstory":"Searching for the truth behind my mentor's disappearance."}'
```

5. Talk to an NPC:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/npc/talk \
  -H "Content-Type: application/json" \
  -d '{"player_id":"player-1","npc_id":"npc-1","message":"Have you seen any scholars pass through recently?"}'
```

## Notes

- If `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` is configured in `.env`, the server will use the configured LLM.
- If no API keys are present, the `/api/v1/action` endpoint still returns a fallback narration.
- Startup tries to connect to PostgreSQL and Redis if configured.
