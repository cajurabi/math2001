"""Content-addressed asset cache.

Layout under the cache root ($COURSE_ASSET_CACHE, default ~/.cache/math2001-course):
    files/<key>.<ext>   the asset itself (mp3, json, mp4, vtt, jpg)
    meta/<key>.json     what produced it: generator, inputs, size, creation time
    models/             downloaded ML models (alignment)

A key is sha256 over the generator id, its version and the canonical JSON of every input that
affects the output, so identical inputs never pay for regeneration twice.
"""

import hashlib
import json
import os
import time
from pathlib import Path


def cache_root() -> Path:
    root = Path(os.environ.get("COURSE_ASSET_CACHE", Path.home() / ".cache" / "math2001-course"))
    (root / "files").mkdir(parents=True, exist_ok=True)
    (root / "meta").mkdir(parents=True, exist_ok=True)
    return root


def content_key(generator: str, version: int, inputs: dict) -> str:
    canonical = json.dumps(
        {"generator": generator, "version": version, "inputs": inputs},
        sort_keys=True, ensure_ascii=False, separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def asset_path(key: str, ext: str) -> Path:
    return cache_root() / "files" / f"{key}.{ext}"


def has(key: str, ext: str) -> bool:
    return asset_path(key, ext).exists()


def store(key: str, ext: str, data: bytes, generator: str, inputs: dict) -> Path:
    """Write an asset atomically, with a metadata record of how it was produced."""
    path = asset_path(key, ext)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)
    meta = {
        "key": key,
        "ext": ext,
        "generator": generator,
        "inputs": inputs,
        "bytes": len(data),
        "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (cache_root() / "meta" / f"{key}.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
    return path


def store_file(key: str, ext: str, source: Path, generator: str, inputs: dict) -> Path:
    return store(key, ext, source.read_bytes(), generator, inputs)
