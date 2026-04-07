from typing import Dict, Any


class QuestTracker:
    async def update_progress(self, quest_id: str, progress: Dict[str, Any]) -> Dict[str, Any]:
        return {"quest_id": quest_id, "progress": progress}

    async def complete_quest(self, quest_id: str) -> Dict[str, Any]:
        return {"quest_id": quest_id, "status": "completed"}


quest_tracker = QuestTracker()
