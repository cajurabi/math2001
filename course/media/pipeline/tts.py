"""Narration audio through OpenRouter's text-to-speech endpoint (ElevenLabs voices)."""

import os
import urllib.error
import urllib.request
import json

from . import cache

GENERATOR = "openrouter-tts"
VERSION = 1

# defaults; an explainer can override them in its EXPLAINER dict
DEFAULT_MODEL = "elevenlabs/eleven-v4"
DEFAULT_VOICE = "george"

# list price in USD per character, for --dry-run estimates (openrouter.ai, 2026-10-21)
PRICE_PER_CHAR = {
    "elevenlabs/eleven-v4": 80 / 1_000_000,
    "elevenlabs/eleven-v4-turbo": 40 / 1_000_000,
    "elevenlabs/eleven-multilingual-v2": 80 / 1_000_000,
    "elevenlabs/eleven-flash-v2.5": 40 / 1_000_000,
}

ENDPOINT = "https://openrouter.ai/api/v1/audio/speech"


def inputs_for(text: str, model: str, voice: str) -> dict:
    return {"text": text, "model": model, "voice": voice, "format": "mp3"}


def key_for(text: str, model: str, voice: str) -> str:
    return cache.content_key(GENERATOR, VERSION, inputs_for(text, model, voice))


def estimated_cost(text: str, model: str) -> float:
    return len(text) * PRICE_PER_CHAR.get(model, 80 / 1_000_000)


def api_key() -> str:
    key = os.environ.get("OPENROUTER_KEY") or os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise SystemExit("tts: set OPENROUTER_KEY (e.g. in .env.local) to generate narration")
    return key


def synthesize(text: str, model: str, voice: str) -> tuple[str, bool]:
    """Return (key, generated) for the mp3 of `text`; calls the API only on a cache miss."""
    key = key_for(text, model, voice)
    if cache.has(key, "mp3"):
        return key, False
    body = json.dumps({"model": model, "input": text, "voice": voice, "response_format": "mp3"}).encode()
    request = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key()}",
            "Content-Type": "application/json",
            "X-Title": "math2001-course media pipeline",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            audio = response.read()
            generation = response.headers.get("X-Generation-Id", "")
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", "replace")[:500]
        raise SystemExit(f"tts: OpenRouter returned HTTP {error.code}: {detail}") from None
    if len(audio) < 1000:
        raise SystemExit(f"tts: suspiciously small response ({len(audio)} bytes) for {text[:60]!r}")
    cache.store(key, "mp3", audio, GENERATOR, {**inputs_for(text, model, voice), "generation_id": generation})
    return key, True
