# INFINITUM Engine

INFINITUM is an AI-led infinite open world engine prototype built with FastAPI and Python. It combines persistent world state, player profiles, NPC interactions, quest generation, and optional LLM-driven storytelling.

## What this project includes

- FastAPI backend with async endpoints
- PostgreSQL persistence for worlds, players, quests, and events
- Redis support for hot cache state
- ChromaDB semantic memory store support
- LLM prompt generation with OpenAI/Anthropic integration and fallback narration
- API key authentication support
- Docker Compose environment for local deployment
- GitHub Actions CI workflow for tests and container builds

## Quick-start

1. Copy the example environment file:

```bash
copy .env.example .env
```

2. Update `.env` with your database and optional LLM keys.

3. Install Python dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Initialize the database schema (if using PostgreSQL):

```bash
python scripts/setup_db.py
```

5. Start the API locally:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

6. Open `http://127.0.0.1:8000/docs` to explore the API.

## Environment variables

Use the `.env.example` file as a template.

- `OPENAI_API_KEY` and `ANTHROPIC_API_KEY`: optional LLM providers
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `API_SECRET_KEY`: API key for protected routes
- `CHROMA_HOST` / `CHROMA_PORT`: ChromaDB host and port
- `EMBEDDING_PROVIDER`: embedding storage provider (default `local`)

## Local development with Docker

The repository contains a `docker-compose.yml` that launches:

- `api` - FastAPI application
- `db` - PostgreSQL database
- `cache` - Redis cache
- `chromadb` - ChromaDB vector store

Run locally with:

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`.

### Database initialization inside Docker

Once the compose stack is running, initialize the database with:

```bash
docker compose exec api python scripts/setup_db.py
```

## Testing

Run the project's test suite locally:

```bash
python -m pytest -q
```

## API endpoints

### Health check

- `GET /health`

### World creation

- `POST /api/v1/world/create`

Example payload:

```json
{
  "character_name": "Asha",
  "character_race": "Human",
  "character_class": "Scholar",
  "character_backstory": "Searching for the truth behind my mentor's disappearance."
}
```

### Player profile

- `GET /api/v1/player/profile?player_id={player_id}`

### Player quests

- `GET /api/v1/player/quests?player_id={player_id}`

### Player action

- `POST /api/v1/action`

Example payload:

```json
{
  "player_id": "player-1",
  "world_id": "world-1",
  "action_text": "I look around the tavern.",
  "action_type": "examine"
}
```

### NPC talk

- `POST /api/v1/npc/talk`

Example payload:

```json
{
  "player_id": "player-1",
  "npc_id": "npc-1",
  "message": "Have you seen any scholars pass through recently?"
}
```

### World map

- `GET /api/v1/world/map/{world_id}`

### Active world events

- `GET /api/v1/world/events?world_id={world_id}`

### Player journal

- `GET /api/v1/player/journal?player_id={player_id}`

### NPC relationship

- `GET /api/v1/npc/{npc_id}/relationship?player_id={player_id}`

### Manual world tick

- `POST /api/v1/world/tick?world_id={world_id}`

## Deployment with GitHub Actions

A GitHub Actions workflow is included at `.github/workflows/ci.yml`.

It runs on `push` and `pull_request` to `main`, executes unit tests, and builds a Docker image. When pushed to `main`, the workflow will publish a container image to GitHub Container Registry at:

```
ghcr.io/<owner>/<repository>/infinitum:latest
```

### Recommended repository secrets

- `GHCR_TOKEN`: GitHub token for container publishing (often `GITHUB_TOKEN` is sufficient)

## Deployment options

### Option 1: GitHub Container Registry

1. Enable GitHub Packages for your repository.
2. Ensure the workflow can push to `ghcr.io`.
3. Use the built image for your chosen cloud provider.

### Option 2: Docker Compose on a VM

1. Copy `.env.example` to `.env` and update values.
2. Run `docker compose up --build`.
3. Point your browser to `http://localhost:8000`.

## How to see the project live

This project is ready to run as a live backend service, but it does not include a hosted public URL by default. To see the software live, host the container on a server or cloud provider and expose port `8000`.

### Run live on a server

1. Push the repository changes to GitHub (already done).
2. Choose a cloud host with Docker support, such as:
   - DigitalOcean App Platform
   - Render
   - Fly.io
   - AWS ECS / Fargate
   - Google Cloud Run
   - Azure App Service
3. Configure the host to use the image built by GitHub Actions or build the Dockerfile directly from the repository.
4. Set environment variables from `.env` or the provider dashboard.
5. Open the provided host URL in a browser.

### Example - using Docker Compose on a remote host

1. SSH into your server.
2. Clone the repository.
3. Copy `.env.example` to `.env` and adjust the settings.
4. Run:

```bash
docker compose up --build -d
```

5. If your server routes port `8000`, open `http://<your-server-ip>:8000`.

### Example - using the GitHub Actions built image

1. The workflow publishes an image to `ghcr.io/<owner>/<repository>/infinitum:latest`.
2. On your host, pull the image:

```bash
docker pull ghcr.io/<owner>/<repository>/infinitum:latest
```

3. Run the container:

```bash
docker run -d -p 8000:8000 \
  -e DATABASE_URL=<your-db> \
  -e REDIS_URL=<your-redis> \
  -e API_SECRET_KEY=<secret-key> \
  ghcr.io/<owner>/<repository>/infinitum:latest
```

4. Open `http://<your-host>:8000`.

## Notes

- If `API_SECRET_KEY` is set, most routes require the header `x-api-key: <API_SECRET_KEY>`.
- If no OpenAI or Anthropic key is configured, `/api/v1/action` still returns a fallback narration.
- The engine supports a mix of persistent database storage and in-memory fallback behavior for local development.
