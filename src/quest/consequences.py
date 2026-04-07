from typing import Dict, Any


class ConsequencePropagator:
    async def apply_immediate(self, consequence_text: str, world_id: str) -> None:
        return

    async def schedule_delayed(self, consequence: Dict[str, Any], world_id: str) -> None:
        return


consequence_propagator = ConsequencePropagator()
