import json
import os
import httpx
from typing import Any

from src.config import settings
from src.brain.prompts import build_action_prompt, build_system_prompt
from src.brain.parser import parse_gm_response


async def _call_openai(system_prompt: str, user_prompt: str) -> str:
    if not settings.openai_api_key:
        raise RuntimeError("OpenAI API key is not configured.")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.openai_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": settings.llm_max_tokens,
        "temperature": settings.llm_temperature,
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


async def _call_anthropic(system_prompt: str, user_prompt: str) -> str:
    if not settings.anthropic_api_key:
        raise RuntimeError("Anthropic API key is not configured.")

    url = "https://api.anthropic.com/v1/complete"
    prompt_text = f"{system_prompt}\n\nHuman: {user_prompt}\n\nAssistant:"
    headers = {
        "x-api-key": settings.anthropic_api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.anthropic_model,
        "prompt": prompt_text,
        "max_tokens_to_sample": settings.llm_max_tokens,
        "temperature": settings.llm_temperature,
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("completion", "")


def _fallback_response(player_action: str) -> str:
    return json.dumps({
        "narration": (
            f"You lean into the room and let your eyes sweep over the tired faces. "
            f"A low murmur of conversation ripples as you speak your intent: '{player_action}'. "
            "The tavern falls into a brief hush, then the innkeeper nods, offering you a place at the table."
        ),
        "scene_mood": "mysterious",
        "location_changed": False,
        "new_location_id": None,
        "time_elapsed_minutes": 10,
        "consequences": [],
        "npcs_interacted": [],
        "quest_updates": [],
        "world_events_triggered": [],
        "suggested_music_mood": "mysterious",
        "ambient_sounds": ["fireplace", "murmur", "rain"]
    })


async def generate_gm_response(context: dict, player_action: str) -> dict:
    system_prompt = build_system_prompt(context)
    user_prompt = build_action_prompt(player_action)

    if settings.anthropic_api_key:
        raw_response = await _call_anthropic(system_prompt, user_prompt)
    elif settings.openai_api_key:
        raw_response = await _call_openai(system_prompt, user_prompt)
    else:
        raw_response = _fallback_response(player_action)

    parsed = parse_gm_response(raw_response)
    return parsed
