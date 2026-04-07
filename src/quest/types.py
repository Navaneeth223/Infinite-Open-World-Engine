from enum import Enum


class QuestType(str, Enum):
    MAIN = "main"
    SIDE = "side"
    FACTION = "faction"
    PERSONAL = "personal"
    EMERGENT = "emergent"
    HIDDEN = "hidden"
    WORLD_EVENT = "world_event"
