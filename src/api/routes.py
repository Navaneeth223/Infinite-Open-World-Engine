import uuid

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.api.auth import get_api_key
from src.api.models import (
    NPCTalkRequest,
    NPCTalkResponse,
    PlayerActionRequest,
    PlayerActionResponse,
    WorldCreationRequest,
    WorldCreationResponse,
    PlayerProfileResponse,
    QuestSummary,
    WorldEvent,
    JournalEntry,
    NPCRelationshipResponse,
    WorldMapResponse,
)
from src.brain.story import generate_gm_response
from src.memory.retrieval import retrieval
from src.quest.generator import quest_generator
from src.world.generator import world_generator
from src.world.state import WorldStateManager

router = APIRouter(dependencies=[Depends(get_api_key)])


@router.post("/api/v1/action", response_model=PlayerActionResponse)
async def player_action(request: PlayerActionRequest) -> PlayerActionResponse:
    context = {
        "world_name": "The Shattered Vale",
        "game_date": "Year 1, Month 1, Day 1, Morning",
        "current_location_name": "The Rusted Anvil Tavern",
        "current_location_description": "A smoke-stained room warmed by a cracked hearth, crowded with travelers and local stubbornness.",
        "current_weather": "cool drizzle",
        "time_of_day": "morning",
        "region_name": "Ashen Crossing",
        "region_description": "A fringe borderland of ash-swept plains and battered stone ruins.",
        "player_name": "Traveler",
        "player_race": "Human",
        "player_class": "Wanderer",
        "player_level": 1,
        "player_health": 100,
        "player_max_health": 100,
        "player_gold": 10,
        "player_global_reputation": 0,
        "player_status_effects": "none",
        "recent_player_history": ["Entered the tavern.", "Listened to a gruff merchant."],
        "active_world_events": ["A caravan went missing to the west."],
        "npcs_present": ["Innkeeper Mara", "A scarred guard", "A nervous scholar"],
        "retrieved_memories": ["You once saved a child from a collapsed bridge."],
        "active_quests": ["Find the missing caravan trader."]
    }

    try:
        player = await WorldStateManager.get_player(request.player_id)
        world = await WorldStateManager.get_world(request.world_id)
        if player and world and player.get("current_location_id"):
            try:
                built_context = await retrieval.build_context(
                    player_id=request.player_id,
                    player_input=request.action_text,
                    location_id=player["current_location_id"],
                    world_id=request.world_id,
                )
                if built_context:
                    context.update({
                        "player_name": player.get("character_name", context["player_name"]),
                        "player_race": player.get("character_race", context["player_race"]),
                        "player_class": player.get("character_class", context["player_class"]),
                        "recent_player_history": built_context.get("recent_actions", context["recent_player_history"]),
                        "active_world_events": [event.get("title", "") for event in built_context.get("relevant_events", [])],
                        "active_quests": [quest.get("title", "") for quest in built_context.get("active_quests", [])],
                        "npcs_present": [npc.get("name", "Unknown") for npc in built_context.get("npcs_present", [])],
                        "retrieved_memories": [memory.get("text", "") for memory in built_context.get("npc_memories", {}).values()],
                    })
            except Exception:
                pass

        response = await generate_gm_response(context, request.action_text)
        return PlayerActionResponse(**response)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/api/v1/world/create", response_model=WorldCreationResponse)
async def create_world(request: WorldCreationRequest) -> WorldCreationResponse:
    world = await world_generator.generate_seed_world(
        character_name=request.character_name,
        character_race=request.character_race,
        character_class=request.character_class,
        character_backstory=request.character_backstory,
    )
    await WorldStateManager.create_world(world)

    player_id = str(uuid.uuid4())
    player = {
        "id": player_id,
        "world_id": world["id"],
        "character_name": request.character_name,
        "character_race": request.character_race,
        "character_class": request.character_class,
        "character_backstory": request.character_backstory,
        "level": 1,
        "experience": 0,
        "health": 100,
        "max_health": 100,
        "gold": 50,
        "current_location_id": world["starting_location"].get("id"),
        "reputation": {"global": 0},
        "status_effects": {},
    }
    await WorldStateManager.create_player(player)

    return WorldCreationResponse(
        world_id=world["id"],
        player_id=player_id,
        world_name=world["name"],
        starting_location=world["starting_location"],
        initial_world_events=world["initial_world_events"],
        main_quest_hook=world["main_quest_hook"],
    )


@router.get("/api/v1/player/profile", response_model=PlayerProfileResponse)
async def get_player_profile(player_id: str) -> PlayerProfileResponse:
    player = await WorldStateManager.get_player(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return PlayerProfileResponse(
        player_id=player_id,
        world_id=player.get("world_id", ""),
        character_name=player.get("character_name", "Unknown"),
        character_race=player.get("character_race", "Unknown"),
        character_class=player.get("character_class", "Unknown"),
        level=player.get("level", 1),
        health=player.get("health", 100),
        max_health=player.get("max_health", 100),
        gold=player.get("gold", 0),
        reputation=player.get("reputation", {}),
        current_location_id=player.get("current_location_id"),
        status_effects=player.get("status_effects", {}),
    )


@router.get("/api/v1/player/quests", response_model=List[QuestSummary])
async def get_player_quests(player_id: str) -> List[QuestSummary]:
    player = await WorldStateManager.get_player(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    world_id = player.get("world_id")
    if not world_id:
        return []

    quest = await quest_generator.generate_emergent_quest({}, {})
    return [QuestSummary(
        title=quest["title"],
        description=quest["description"],
        status="active",
        difficulty=quest.get("difficulty", 3),
    )]


@router.post("/api/v1/npc/talk", response_model=NPCTalkResponse)
async def talk_to_npc(request: NPCTalkRequest) -> NPCTalkResponse:
    dialogue = (
        "The NPC pauses, then offers you a steady look. 'I have heard rumors of your arrival, and I have a question for you.'"
    )
    return NPCTalkResponse(
        dialogue=dialogue,
        tone="suspicious",
        body_language="The NPC leans back slightly, eyes narrowed.",
        relationship_delta=0,
        secret_proximity=0.2,
        offers_quest=False,
        quest_hint=None,
        memory_update="The NPC now knows you asked about their rumors.",
    )


@router.get("/api/v1/world/events", response_model=List[WorldEvent])
async def get_world_events(world_id: str, discovered_only: bool = True) -> List[WorldEvent]:
    events = await WorldStateManager.get_active_world_events(world_id)
    return [WorldEvent(**event) for event in events]


@router.get("/api/v1/player/journal", response_model=List[JournalEntry])
async def get_journal(player_id: str) -> List[JournalEntry]:
    journal = await WorldStateManager.get_player_journal(player_id)
    return [JournalEntry(**entry) for entry in journal]


@router.get("/api/v1/npc/{npc_id}/relationship", response_model=NPCRelationshipResponse)
async def get_npc_relationship(npc_id: str, player_id: str) -> NPCRelationshipResponse:
    npc_rel = await WorldStateManager.get_npc_relationship(npc_id, player_id)
    if not npc_rel:
        raise HTTPException(status_code=404, detail="NPC not found")
    return NPCRelationshipResponse(
        npc_id=npc_id,
        player_relationship_score=npc_rel.get("player_relationship_score", 0),
        player_relationship_label=npc_rel.get("player_relationship_label", "stranger"),
        times_met=npc_rel.get("times_met", 0),
        last_seen_game_date=npc_rel.get("last_seen_game_date"),
        remembered_events=[],
    )


@router.post("/api/v1/world/tick")
async def manual_tick(world_id: str):
    tick_result = await WorldStateManager.tick_world(world_id)
    return tick_result


@router.get("/api/v1/world/map/{world_id}", response_model=WorldMapResponse)
async def get_world_map(world_id: str, discovered_only: bool = True) -> WorldMapResponse:
    world_map = await WorldStateManager.get_world_map(world_id, discovered_only)
    if not world_map:
        raise HTTPException(status_code=404, detail="World not found")
    return WorldMapResponse(**world_map)
