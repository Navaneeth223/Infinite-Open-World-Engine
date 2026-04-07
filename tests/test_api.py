import json
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)
API_HEADERS = {"x-api-key": "secret-key"}


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_world_create_endpoint():
    response = client.post(
        "/api/v1/world/create",
        headers=API_HEADERS,
        json={
            "character_name": "Asha",
            "character_race": "Human",
            "character_class": "Scholar",
            "character_backstory": "Searching for the truth behind my mentor's disappearance.",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "world_id" in data
    assert data["world_name"]
    assert "starting_location" in data


def test_world_create_and_retrieve_world_map():
    create_response = client.post(
        "/api/v1/world/create",
        headers=API_HEADERS,
        json={
            "character_name": "Asha",
            "character_race": "Human",
            "character_class": "Scholar",
            "character_backstory": "Searching for the truth behind my mentor's disappearance.",
        },
    )
    assert create_response.status_code == 200
    world_id = create_response.json()["world_id"]

    map_response = client.get(f"/api/v1/world/map/{world_id}", headers=API_HEADERS)
    assert map_response.status_code == 200
    map_data = map_response.json()
    assert map_data["world_id"] == world_id
    assert isinstance(map_data["regions"], list)
    assert isinstance(map_data["locations"], list)
    assert map_data["locations"]


def test_manual_tick_endpoint_returns_ok_for_created_world():
    create_response = client.post(
        "/api/v1/world/create",
        headers=API_HEADERS,
        json={
            "character_name": "Asha",
            "character_race": "Human",
            "character_class": "Scholar",
            "character_backstory": "Searching for the truth behind my mentor's disappearance.",
        },
    )
    assert create_response.status_code == 200
    world_id = create_response.json()["world_id"]

    response = client.post(f"/api/v1/world/tick?world_id={world_id}", headers=API_HEADERS)
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ticked"
    assert payload["world_id"] == world_id
    assert "new_game_date" in payload


def test_world_events_endpoint_returns_list():
    response = client.get("/api/v1/world/events?world_id=world-1", headers=API_HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_player_journal_endpoint_returns_list():
    response = client.get("/api/v1/player/journal?player_id=player-1", headers=API_HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_npc_relationship_endpoint_returns_404_when_missing():
    response = client.get(
        "/api/v1/npc/npc-1/relationship?player_id=player-1",
        headers=API_HEADERS,
    )
    assert response.status_code == 404


def test_world_map_endpoint_returns_404_when_missing():
    response = client.get("/api/v1/world/map/world-1", headers=API_HEADERS)
    assert response.status_code == 404


def test_manual_tick_endpoint_returns_ok():
    response = client.post("/api/v1/world/tick?world_id=world-1", headers=API_HEADERS)
    assert response.status_code == 200
    assert response.json().get("status") == "ticked"


def test_action_requires_api_key():
    response = client.post(
        "/api/v1/action",
        json={
            "player_id": "player-1",
            "world_id": "world-1",
            "action_text": "I look around the tavern.",
            "action_type": "examine",
        },
    )
    assert response.status_code == 401


def test_player_action_endpoint():
    response = client.post(
        "/api/v1/action",
        headers=API_HEADERS,
        json={
            "player_id": "player-1",
            "world_id": "world-1",
            "action_text": "I look around the tavern.",
            "action_type": "examine",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "narration" in data
    assert data["scene_mood"] in ["tense", "peaceful", "mysterious", "dangerous", "melancholic", "joyful", "ominous"]


def test_npc_talk_endpoint():
    response = client.post(
        "/api/v1/npc/talk",
        headers=API_HEADERS,
        json={"player_id": "player-1", "npc_id": "npc-1", "message": "Have you seen any scholars pass through recently?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "dialogue" in data
    assert data["relationship_delta"] == 0
