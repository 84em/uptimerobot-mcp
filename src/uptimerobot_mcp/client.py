"""UptimeRobot API v2 async client."""

import os

import httpx
from dotenv import load_dotenv

load_dotenv()

UPTIMEROBOT_API_BASE = "https://api.uptimerobot.com/v2"


def _get_api_key() -> str:
    key = os.environ.get("UPTIMEROBOT_API_KEY", "").strip()
    if not key:
        raise ValueError(
            "UPTIMEROBOT_API_KEY environment variable is not set. "
            "Set it in your environment or in a .env file."
        )
    return key


async def call_api(endpoint: str, params: dict) -> dict:
    """Make an authenticated POST request to the UptimeRobot API v2."""
    api_key = _get_api_key()
    payload = {"api_key": api_key, "format": "json", **params}

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{UPTIMEROBOT_API_BASE}/{endpoint}",
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()

    result = response.json()

    if result.get("stat") == "fail":
        error = result.get("error", {})
        message = error.get("message", "Unknown error")
        error_type = error.get("type", "unknown")
        raise ValueError(f"UptimeRobot API error [{error_type}]: {message}")

    return result
