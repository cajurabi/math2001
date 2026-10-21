"""Week 1 Day 1 explainer: reading a Lean `calc` block (Example 1.2.1)."""

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline.narration import NarratedScene  # noqa: E402

EXPLAINER = {"id": "w01d1/reading-calc", "title": "Reading a Lean calc block", "scene": "ReadingCalc"}

NARRATION = {
    "same": "Here's the same proof, written in Lean. It looks different, but it's the same three steps.",
    "statement": "The first two lines say what we're proving. h one and h two are names for the facts we "
                 "were given: a minus b equals four, and a times b equals one. After them comes the goal.",
    "calc": "The word calc starts a chain of equalities. Each underscore means: the expression we "
            "ended with, on the line before.",
    "ring": "After each step comes its justification. By ring means: this step is pure algebra, so Lean "
            "checks it by expanding both sides.",
    "rw": "By r w means rewrite, which is substitution. Rewriting with h one and h two swaps in the two "
          "facts, exactly like on paper.",
    "check": "If a justification is wrong, Lean underlines it in red. When every link checks out, the "
             "proof is complete.",
}

MONO = "Noto Sans Mono"
ALGEBRA = TEAL_C
SUBST = GOLD_C
KNOWN_A = BLUE_C
KNOWN_B = YELLOW_C

LINES = [
    "example {a b : ℚ} (h1 : a - b = 4) (h2 : a * b = 1) :",
    "    (a + b) ^ 2 = 20 :=",
    "  calc",
    "    (a + b) ^ 2 = (a - b) ^ 2 + 4 * (a * b) := by ring",
    "    _ = 4 ^ 2 + 4 * 1 := by rw [h1, h2]",
    "    _ = 20 := by ring",
]


def part(line_mob: Text, line: str, sub: str, occurrence: int = 1) -> VGroup:
    """The glyphs of `sub` inside a Text line (Text has one submobject per non-space character)."""
    index = -1
    for _ in range(occurrence):
        index = line.index(sub, index + 1)
    start = len(line[:index].replace(" ", ""))
    return VGroup(*line_mob[start:start + len(sub.replace(" ", ""))])


class ReadingCalc(NarratedScene):
    def construct(self):
        code = VGroup(*(Text(line, font=MONO, font_size=26) for line in LINES))
        code.arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        # keep the leading indentation that Text drops
        char_width = Text("x", font=MONO, font_size=26).width * 1.06
        for mob, line in zip(code, LINES):
            mob.shift(RIGHT * char_width * (len(line) - len(line.lstrip(" "))))
        code.move_to(UP * 0.5).to_edge(LEFT, buff=0.6)
        line = dict(enumerate(LINES))

        with self.beat("same") as beat:
            self.play(LaggedStart(*(FadeIn(m, shift=RIGHT * 0.2) for m in code), lag_ratio=0.25),
                      run_time=beat.until("It"))
            steps = VGroup(*(SurroundingRectangle(code[i], color=GREY_B, buff=0.08) for i in (3, 4, 5)))
            self.play(LaggedStart(*(Create(s) for s in steps), lag_ratio=0.3), run_time=beat.until("three") + 0.5)
            self.play(FadeOut(steps))

        with self.beat("statement") as beat:
            h1 = part(code[0], line[0], "(h1 : a - b = 4)")
            h2 = part(code[0], line[0], "(h2 : a * b = 1)")
            goal = part(code[1], line[1], "(a + b) ^ 2 = 20")
            box1 = SurroundingRectangle(h1, color=KNOWN_A, buff=0.06)
            box2 = SurroundingRectangle(h2, color=KNOWN_B, buff=0.06)
            note1 = MathTex("a-b=4", color=KNOWN_A).scale(0.8).next_to(box1, UP, buff=0.15)
            note2 = MathTex("ab=1", color=KNOWN_B).scale(0.8).next_to(box2, UP, buff=0.15)
            self.play(Create(box1), FadeIn(note1), h1.animate.set_color(KNOWN_A), run_time=beat.until("and", 2))
            self.play(Create(box2), FadeIn(note2), h2.animate.set_color(KNOWN_B), run_time=beat.until("After"))
            goal_box = SurroundingRectangle(goal, color=WHITE, buff=0.06)
            self.play(Create(goal_box), run_time=beat.until("goal"))
            self.play(FadeOut(note1), FadeOut(note2), FadeOut(box1), FadeOut(box2), FadeOut(goal_box))

        with self.beat("calc") as beat:
            calc_word = part(code[2], line[2], "calc")
            self.play(calc_word.animate.set_color(PURPLE_B), Indicate(calc_word, color=PURPLE_B),
                      run_time=beat.until("Each"))
            under1 = part(code[4], line[4], "_")
            prev1 = part(code[3], line[3], "(a - b) ^ 2 + 4 * (a * b)")
            u_box = SurroundingRectangle(under1, color=WHITE, buff=0.06)
            p_box = SurroundingRectangle(prev1, color=WHITE, buff=0.06)
            arrow = CurvedArrow(u_box.get_top() + UP * 0.03, p_box.get_bottom() + DOWN * 0.03,
                                angle=-TAU / 8, color=WHITE, stroke_width=3)
            self.play(Create(u_box), run_time=beat.until("expression"))
            self.play(Create(arrow), Create(p_box), run_time=beat.until("before"))
            self.play(FadeOut(u_box), FadeOut(p_box), FadeOut(arrow))

        with self.beat("ring") as beat:
            rings = [part(code[3], line[3], "by ring"), part(code[5], line[5], "by ring")]
            self.play(*(r.animate.set_color(ALGEBRA) for r in rings), run_time=beat.until("means"))
            tags = VGroup(*(Text("algebra", font_size=26, color=ALGEBRA).next_to(r, RIGHT, buff=0.4) for r in rings))
            self.play(LaggedStart(*(FadeIn(t, shift=LEFT * 0.2) for t in tags), lag_ratio=0.3),
                      run_time=beat.until("checks"))

        with self.beat("rw") as beat:
            rw = part(code[4], line[4], "by rw [h1, h2]")
            tag = Text("substitution", font_size=26, color=SUBST).next_to(rw, RIGHT, buff=0.4)
            self.play(rw.animate.set_color(SUBST), FadeIn(tag, shift=LEFT * 0.2), run_time=beat.until("Rewriting"))
            link1 = CurvedArrow(h1.get_bottom(), part(code[4], line[4], "h1").get_top(), angle=TAU / 6, color=KNOWN_A)
            link2 = CurvedArrow(h2.get_bottom(), part(code[4], line[4], "h2").get_top(), angle=TAU / 8, color=KNOWN_B)
            self.play(Create(link1), Create(link2), run_time=beat.until("exactly"))
            self.play(FadeOut(link1), FadeOut(link2))

        with self.beat("check") as beat:
            target = rings[0]
            wrong = Text("by rw", font=MONO, font_size=26, color=SUBST).move_to(target, aligned_edge=LEFT)
            squiggle = FunctionGraph(lambda x: 0.04 * np.sin(14 * x), x_range=[0, wrong.width], color=RED)
            squiggle.next_to(wrong, DOWN, buff=0.04).align_to(wrong, LEFT)
            self.play(FadeOut(target), FadeIn(wrong), run_time=beat.until("Lean"))
            self.play(Create(squiggle), run_time=beat.until("When"))
            self.play(FadeOut(wrong), FadeOut(squiggle), FadeIn(target))
            done = Text("Proof complete ✓", font_size=34, color=GREEN_C).next_to(code, DOWN, buff=0.7).align_to(code, LEFT)
            self.play(Write(done), run_time=beat.until("complete"))
        self.wait(0.8)
