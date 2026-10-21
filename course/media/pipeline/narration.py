"""Narrated Manim scenes, synced to cached narration audio.

An explainer scene subclasses NarratedScene and wraps its animations in beats:

    with self.beat("substitute") as beat:
        self.play(Write(line2), run_time=beat.until("swap"))   # finish as the word "swap" is said
        self.play(Indicate(h1))                               # then keep animating
    # leaving the block waits out the rest of the clip

build.py synthesizes and aligns every beat before rendering, and passes this scene a manifest
(beat id → audio file, duration, word timings) through $MEDIA_NARRATION_MANIFEST. The scene
writes back when each beat actually started ($MEDIA_TIMELINE_OUT), which build.py uses to
place captions. It also reports anything left past the frame edge at the end of a beat
("offscreen"), which build.py prints, so clipped labels are caught before review.
"""

import json
import os
from contextlib import contextmanager
from dataclasses import dataclass

from manim import Scene, config

EDGE_SLACK = 0.02  # scene units a mobject may overhang the frame before it is reported


@dataclass
class Beat:
    id: str
    text: str
    audio: str
    duration: float
    words: list[dict]
    scene: "NarratedScene"
    start: float = 0.0

    def elapsed(self) -> float:
        return self.scene.renderer.time - self.start

    def remaining(self) -> float:
        return max(0.0, self.duration - self.elapsed())

    def word_time(self, word: str, occurrence: int = 1) -> float:
        """Seconds from the start of the beat to when `word` begins being spoken."""
        target = word.lower().strip(".,!?;:")
        seen = 0
        for w in self.words:
            if w["word"].lower().strip(".,!?;:\"'") == target:
                seen += 1
                if seen == occurrence:
                    return w["start"]
        raise KeyError(f"beat {self.id!r}: word {word!r} (#{occurrence}) not in narration")

    def until(self, word: str, occurrence: int = 1, minimum: float = 0.2) -> float:
        """Run time that ends an animation (started now) as `word` is spoken."""
        return max(minimum, self.word_time(word, occurrence) - self.elapsed())


class NarratedScene(Scene):
    def setup(self):
        manifest_path = os.environ.get("MEDIA_NARRATION_MANIFEST")
        if not manifest_path:
            raise RuntimeError("NarratedScene must be rendered by pipeline.build (no narration manifest)")
        self._narration = json.loads(open(manifest_path, encoding="utf-8").read())
        self._timeline: list[dict] = []
        self._offscreen: list[dict] = []

    @contextmanager
    def beat(self, beat_id: str):
        spec = self._narration[beat_id]
        current = Beat(beat_id, spec["text"], spec["audio"], spec["duration"], spec["words"], self)
        current.start = self.renderer.time
        self.add_sound(current.audio)
        self._timeline.append({"beat": beat_id, "start": round(current.start, 3)})
        yield current
        self._check_frame(beat_id)
        if current.remaining() > 0.01:
            self.wait(current.remaining())

    def _check_frame(self, beat_id: str):
        """Record each text (or other top-level mobject) on screen that reaches past the frame."""
        half_w, half_h = config.frame_width / 2, config.frame_height / 2
        seen = set()
        for top in self.mobjects:
            labelled = [m for m in top.get_family() if hasattr(m, "tex_string") or hasattr(m, "text")]
            for m in labelled or [top]:
                if id(m) in seen or m.has_no_points() and not m.submobjects:
                    continue
                seen.add(id(m))
                left, right = m.get_left()[0], m.get_right()[0]
                bottom, top_y = m.get_bottom()[1], m.get_top()[1]
                over = max(-half_w - left, right - half_w, -half_h - bottom, top_y - half_h)
                if over > EDGE_SLACK:
                    label = getattr(m, "text", None) or getattr(m, "tex_string", None) or type(m).__name__
                    self._offscreen.append({"beat": beat_id, "what": str(label)[:60], "over": round(float(over), 2)})

    def tear_down(self):
        out = os.environ.get("MEDIA_TIMELINE_OUT")
        if out:
            with open(out, "w", encoding="utf-8") as f:
                json.dump({"timeline": self._timeline, "total": round(self.renderer.time, 3),
                           "offscreen": self._offscreen}, f)
