from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PlayerActionRequest(BaseModel):
    player_id: str
    world_id: str
    action_text: str
    action_type: Optional[str] = Field(default="custom")


class WorldCreationRequest(BaseModel):
    character_name: str
    character_race: str
    character_class: str
    character_backstory: str


class NPCInteraction(BaseModel):
    npc_id: str
    interaction_type: str
    relationship_delta: int
    memory_to_store: Optional[str] = None


class Consequence(BaseModel):
    type: str
    target_id: Optional[str] = None
    description: str
    severity: Optional[int] = None


class QuestUpdate(BaseModel):
    quest_id: Optional[str] = None
    action: str
    details: Dict[str, Any] = Field(default_factory=dict)


class WorldEventTriggered(BaseModel):
    event_type: str
    title: str
    description: str
    affected_locations: List[str] = Field(default_factory=list)
    delayed_hours: int = 0


class PlayerActionResponse(BaseModel):
    narration: str
    scene_mood: str
    location_changed: bool = False
    new_location_id: Optional[str] = None
    time_elapsed_minutes: int = 10
    consequences: List[Consequence] = Field(default_factory=list)
    npcs_interacted: List[NPCInteraction] = Field(default_factory=list)
    quest_updates: List[QuestUpdate] = Field(default_factory=list)
    world_events_triggered: List[WorldEventTriggered] = Field(default_factory=list)
    suggested_music_mood: str = "mysterious"
    ambient_sounds: List[str] = Field(default_factory=list)


class WorldCreationResponse(BaseModel):
    world_id: str
    world_name: str
    starting_location: Dict[str, Any]
    initial_world_events: List[Dict[str, Any]]
    main_quest_hook: Dict[str, Any]


class WorldEvent(BaseModel):
    id: Optional[str] = None
    event_type: str
    title: str
    description: str
    location_id: Optional[str] = None
    region_id: Optional[str] = None
    affected_factions: Optional[List[str]] = None
    caused_by_player: bool = False
    game_date: Optional[Dict[str, Any]] = None
    resolved: bool = False


class JournalEntry(BaseModel):
    id: Optional[str] = None
    player_id: str
    entry_type: str
    title: Optional[str] = None
    content: str
    game_date: Optional[Dict[str, Any]] = None
    real_timestamp: Optional[str] = None


class NPCRelationshipResponse(BaseModel):
    npc_id: str
    player_relationship_score: int
    player_relationship_label: str
    times_met: int
    last_seen_game_date: Optional[Dict[str, Any]] = None
    remembered_events: List[str] = Field(default_factory=list)


class WorldMapResponse(BaseModel):
    world_id: str
    world_name: str
    regions: List[Dict[str, Any]]
    locations: List[Dict[str, Any]]


class NPCTalkRequest(BaseModel):
    player_id: str
    npc_id: str
    message: str


class NPCTalkResponse(BaseModel):
    dialogue: str
    tone: str
    body_language: str
    relationship_delta: int
    secret_proximity: float
    offers_quest: bool = False
    quest_hint: Optional[str] = None
    memory_update: Optional[str] = None
