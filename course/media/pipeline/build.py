"""Build every explainer: narrate (TTS) → align → render (Manim) → captions + poster.

    python -m pipeline.build              build what's missing, update course/assets.lock.json
    python -m pipeline.build --dry-run    report what would be generated and what it would cost
    python -m pipeline.build --only w01d1/calc-chain --quality draft

Each explainer module in explainers/ defines:
    EXPLAINER = {"id": "w01d1/calc-chain", "title": "...", "scene": "CalcChain"}   (+ optional "model", "voice")
    NARRATION = {"beat-id": "Text to speak.", ...}                                  (in order)
and a NarratedScene subclass named by EXPLAINER["scene"].
"""

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import manim

from . import PIPELINE_VERSION, align, cache, captions, cues, tts

MEDIA_DIR = Path(__file__).resolve().parent.parent
EXPLAINERS_DIR = MEDIA_DIR / "explainers"
LOCK_PATH = MEDIA_DIR.parent / "assets.lock.json"
RENDER_GENERATOR = "manim-render"

QUALITY = {
    "high": ["-r", "1920,1080", "--frame_rate", "30"],
    "draft": ["-r", "854,480", "--frame_rate", "15"],
}


def load_explainers(only: str | None):
    modules = []
    for path in sorted(EXPLAINERS_DIR.glob("*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if only and module.EXPLAINER["id"] != only:
            continue
        modules.append((path, module))
    if only and not modules:
        raise SystemExit(f"build: no explainer with id {only!r}")
    return modules


def sha_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audio_duration(path: Path) -> float:
    import av

    with av.open(str(path)) as container:
        return container.duration / 1_000_000


def video_key(path: Path, audio_keys: list[str], align_keys: list[str], quality: str) -> str:
    return cache.content_key(RENDER_GENERATOR, PIPELINE_VERSION, {
        "manim": manim.__version__,
        "quality": quality,
        "scene_source": sha_of(path),
        "narration_lib": sha_of(Path(__file__).with_name("narration.py")),
        "captions_lib": sha_of(Path(__file__).with_name("captions.py")),
        "audio": audio_keys,
        "alignment": align_keys,
    })


def write_poster(video: Path, out: Path):
    import av

    with av.open(str(video)) as container:
        stream = container.streams.video[0]
        target = float(stream.duration * stream.time_base) * 0.6 if stream.duration else 5.0
        for frame in container.decode(stream):
            if frame.time is not None and frame.time >= target:
                frame.to_image().save(out, quality=85)
                return
    raise RuntimeError(f"poster: no frame decoded from {video}")


def render(path: Path, module, beats: dict, quality: str) -> tuple[Path, dict, Path]:
    work = Path(tempfile.mkdtemp(prefix="render-"))
    manifest = work / "narration.json"
    timeline = work / "timeline.json"
    manifest.write_text(json.dumps(beats, ensure_ascii=False))
    scene = module.EXPLAINER["scene"]
    command = ["manim", "render", *QUALITY[quality], "--media_dir", str(work / "media"),
               "--disable_caching", "--progress_bar", "none", str(path), scene]
    env = {**__import__("os").environ, "MEDIA_NARRATION_MANIFEST": str(manifest), "MEDIA_TIMELINE_OUT": str(timeline)}
    print(f"  rendering {scene} ({quality}) …", flush=True)
    subprocess.run(command, check=True, env=env, cwd=EXPLAINERS_DIR)
    videos = list((work / "media" / "videos").rglob(f"{scene}.mp4"))
    if not videos:
        raise SystemExit(f"build: manim produced no {scene}.mp4")
    return videos[0], json.loads(timeline.read_text()), work


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="report only; no API calls, no rendering")
    parser.add_argument("--only", help="build a single explainer id")
    parser.add_argument("--quality", choices=QUALITY, default="high")
    args = parser.parse_args(argv)

    lock = json.loads(LOCK_PATH.read_text()) if LOCK_PATH.exists() else {}
    total_cost = 0.0
    total_chars = 0
    rendered = 0

    for path, module in load_explainers(args.only):
        info = module.EXPLAINER
        model = info.get("model", tts.DEFAULT_MODEL)
        voice = info.get("voice", tts.DEFAULT_VOICE)
        print(f"{info['id']}: {info['title']}  [{model}, voice {voice}]")
        cue_problems = cues.problems(path)
        for problem in cue_problems:
            print(f"  cue: {problem}")
        if cue_problems:
            raise SystemExit(f"build: fix the cue words in {path.name} first (nothing was synthesized)")

        audio_keys = [tts.key_for(text, model, voice) for text in module.NARRATION.values()]
        missing = [(beat, text) for (beat, text), key in zip(module.NARRATION.items(), audio_keys)
                   if not cache.has(key, "mp3")]
        chars = sum(len(text) for _, text in missing)
        cost = sum(tts.estimated_cost(text, model) for _, text in missing)
        total_chars += chars
        total_cost += cost
        print(f"  narration: {len(module.NARRATION)} beats, {len(missing)} to synthesize "
              f"({chars} chars, ~${cost:.3f})")

        if args.dry_run:
            align_keys = [align.key_for(k, t) for k, t in zip(audio_keys, module.NARRATION.values())]
            key = video_key(path, audio_keys, align_keys, args.quality)
            print(f"  video: {'cached' if cache.has(key, 'mp4') else 'would render'} ({key[:12]})")
            continue

        beats = {}
        align_keys = []
        for beat_id, text in module.NARRATION.items():
            audio_key, generated = tts.synthesize(text, model, voice)
            if generated:
                print(f"    synthesized {beat_id!r}")
            align_key, words, aligned = align.align(audio_key, text)
            if aligned:
                print(f"    aligned {beat_id!r} ({len(words)} words)")
            align_keys.append(align_key)
            audio = cache.asset_path(audio_key, "mp3")
            beats[beat_id] = {"text": text, "audio": str(audio), "duration": audio_duration(audio), "words": words}

        key = video_key(path, [tts.key_for(t, model, voice) for t in module.NARRATION.values()], align_keys, args.quality)
        if cache.has(key, "mp4") and cache.has(key, "vtt") and cache.has(key, "jpg"):
            print(f"  video: cached ({key[:12]})")
            meta = json.loads((cache.cache_root() / "meta" / f"{key}.json").read_text())
            duration = meta["inputs"].get("duration", 0)
        else:
            video, timeline, work = render(path, module, beats, args.quality)
            inputs = {"explainer": info["id"], "quality": args.quality, "duration": timeline["total"]}
            cache.store_file(key, "mp4", video, RENDER_GENERATOR, inputs)
            cache.store(key, "vtt", captions.build_vtt(timeline["timeline"], beats).encode(), RENDER_GENERATOR, inputs)
            poster = work / "poster.jpg"
            write_poster(video, poster)
            cache.store_file(key, "jpg", poster, RENDER_GENERATOR, inputs)
            duration = timeline["total"]
            rendered += 1
            print(f"  video: rendered {duration:.1f}s ({key[:12]})")

        lock[info["id"]] = {
            "title": info["title"],
            "key": key,
            "files": {"video": f"{key}.mp4", "captions": f"{key}.vtt", "poster": f"{key}.jpg"},
            "durationSeconds": round(duration, 1),
            "transcript": list(module.NARRATION.values()),
            "narration": {"model": model, "voice": voice, "audio": dict(zip(module.NARRATION, (tts.key_for(t, model, voice) for t in module.NARRATION.values())))},
        }

    if args.dry_run:
        print(f"\ndry run: {total_chars} chars to synthesize, estimated ${total_cost:.3f}; nothing generated")
        return
    LOCK_PATH.write_text(json.dumps(dict(sorted(lock.items())), indent=2, ensure_ascii=False) + "\n")
    print(f"\ndone: {total_chars} chars synthesized (~${total_cost:.3f}), {rendered} video(s) rendered; "
          f"lock file updated: {LOCK_PATH.name}")


if __name__ == "__main__":
    sys.exit(main())
