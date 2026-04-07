from typing import Dict, Any


class EconomyEngine:
    async def update_market(self, world_id: str) -> None:
        return

    def apply_price_drift(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        market_data["current_price"] = int(market_data.get("current_price", 0) * 1.02)
        return market_data


economy_engine = EconomyEngine()
