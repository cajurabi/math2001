"""WebVTT captions from the aligned narration and the rendered beat timeline."""

MAX_WORDS = 12
SENTENCE_END = (".", "?", "!", ":", ";")


def _timestamp(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def build_vtt(timeline: list[dict], beats: dict[str, dict]) -> str:
    """timeline: [{"beat", "start"}] from the render; beats: beat id → {"words": [...]}."""
    cues = []
    for entry in timeline:
        words = beats[entry["beat"]]["words"]
        offset = entry["start"]
        chunk: list[dict] = []
        for i, word in enumerate(words):
            chunk.append(word)
            last = i == len(words) - 1
            if last or len(chunk) >= MAX_WORDS or word["word"].endswith(SENTENCE_END):
                text = " ".join(w["word"] for w in chunk)
                cues.append((offset + chunk[0]["start"], offset + chunk[-1]["end"], text))
                chunk = []
    lines = ["WEBVTT", ""]
    for n, (start, end, text) in enumerate(cues, 1):
        lines += [str(n), f"{_timestamp(start)} --> {_timestamp(max(end, start + 0.5))}", text, ""]
    return "\n".join(lines)
