"""Word timestamps for narration by forced alignment (we know the exact script, so we align
rather than transcribe). Runs locally with stable-ts; results are cached by audio key."""

import json
import os

from . import cache

GENERATOR = "stable-ts-align"
VERSION = 1
MODEL = "base.en"

_model = None


def key_for(audio_key: str, text: str) -> str:
    return cache.content_key(GENERATOR, VERSION, {"audio": audio_key, "text": text, "model": MODEL})


def _load_model():
    global _model
    if _model is None:
        os.environ.setdefault("XDG_CACHE_HOME", str(cache.cache_root() / "models"))
        import stable_whisper  # heavy import: only when an alignment is actually needed

        _model = stable_whisper.load_model(MODEL, device="cpu")
    return _model


def align(audio_key: str, text: str) -> tuple[str, list[dict], bool]:
    """Return (key, words, generated); words are {"word", "start", "end"} in seconds."""
    key = key_for(audio_key, text)
    if cache.has(key, "json"):
        return key, json.loads(cache.asset_path(key, "json").read_text()), False
    result = _load_model().align(str(cache.asset_path(audio_key, "mp3")), text, language="en")
    words = [
        {"word": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)}
        for segment in result.segments
        for w in segment.words
        if w.word.strip()
    ]
    cache.store(key, "json", json.dumps(words).encode(), GENERATOR, {"audio": audio_key, "text": text, "model": MODEL})
    return key, words, True
