import asyncio
import json
from fastapi import WebSocket
from src.brain.story import generate_gm_response


async def stream_narration(websocket: WebSocket, context: dict, player_action: str):
    await websocket.accept()
    try:
        response = await generate_gm_response(context, player_action)
        await websocket.send_json({"type": "game_state", "content": response})
    except Exception as exc:
        await websocket.send_json({"type": "error", "content": str(exc)})
    finally:
        await websocket.close()
