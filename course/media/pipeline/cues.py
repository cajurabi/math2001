"""Static check of an explainer's cue words, before any narration is bought or frames rendered.

Animations end on spoken words: `beat.until("word", n)` and `self.show(beat, "word", ..., occurrence=n)`
name the n-th time that word is spoken in the beat. A missing word fails the render; an occurrence
that comes before the previous cue's gives a 0.2 s animation. The narration is the text in NARRATION,
so both are checked here against it, and the beats must run in NARRATION's order (it is also the
transcript's order).

    python -m pipeline.cues explainers/w01d1_brahmagupta.py
"""

import ast
import sys
from pathlib import Path


def _words(text: str) -> list[str]:
    # the same normalisation as Beat.word_time
    return [w.lower().strip(".,!?;:\"'") for w in text.split()]


def _cue(call: ast.Call) -> tuple[str, int] | None:
    attr = getattr(call.func, "attr", "")
    keywords = {k.arg: k.value for k in call.keywords}
    if attr == "until" and call.args and isinstance(call.args[0], ast.Constant):
        occurrence = call.args[1] if len(call.args) > 1 else keywords.get("occurrence")
        return call.args[0].value, occurrence.value if isinstance(occurrence, ast.Constant) else 1
    if attr == "show" and len(call.args) > 1 and isinstance(call.args[1], ast.Constant):
        occurrence = keywords.get("occurrence")
        return call.args[1].value, occurrence.value if isinstance(occurrence, ast.Constant) else 1
    return None


def problems(path: Path) -> list[str]:
    tree = ast.parse(path.read_text())
    narration = next((ast.literal_eval(node.value) for node in ast.walk(tree)
                      if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "NARRATION"), None)
    if narration is None:
        return [f"{path.name}: no NARRATION"]
    found, order = [], []
    for node in ast.walk(tree):
        if not isinstance(node, ast.With):
            continue
        context = node.items[0].context_expr
        if not (isinstance(context, ast.Call) and getattr(context.func, "attr", "") == "beat"):
            continue
        beat = context.args[0].value
        order.append((node.lineno, beat))
        if beat not in narration:
            found.append(f"line {node.lineno}: beat {beat!r} has no narration")
            continue
        words = _words(narration[beat])
        cues = sorted((call.lineno, *cue) for call in ast.walk(node)
                      if isinstance(call, ast.Call) and (cue := _cue(call)))
        last = -1
        for lineno, word, occurrence in cues:
            positions = [i for i, w in enumerate(words) if w == word.lower()]
            if len(positions) < occurrence:
                found.append(f"line {lineno}: beat {beat!r} says {word!r} {len(positions)} time(s), cue wants #{occurrence}")
                continue
            position = positions[occurrence - 1]
            if position <= last:
                context_words = " ".join(words[max(0, position - 4):position + 2])
                found.append(f"line {lineno}: beat {beat!r} cue {word!r} #{occurrence} (…{context_words}…) "
                             f"comes before the previous cue")
            last = position
    beats = [beat for _, beat in sorted(order)]
    if beats != list(narration):
        found.append(f"beats run as {beats}, but NARRATION is ordered {list(narration)}")
    return found


if __name__ == "__main__":
    bad = False
    for arg in sys.argv[1:]:
        for problem in problems(Path(arg)):
            print(f"{arg}: {problem}")
            bad = True
    sys.exit(1 if bad else 0)
