"""Week 1 Day 1 explainer: what a proof by calculation is (Example 1.1.1)."""

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline.narration import NarratedScene  # noqa: E402

EXPLAINER = {"id": "w01d1/calc-chain", "title": "What is a proof by calculation?", "scene": "CalcChain"}

NARRATION = {
    "puzzle": "Here's a puzzle. We have two numbers, a and b. We know that a minus b equals four, "
              "and a times b equals one. What is a plus b, all squared?",
    "shortcut": "You could try to solve for a and b first. But there's a shortcut: rewrite what you want "
                "in terms of what you know.",
    "algebra": "Step one is pure algebra. a plus b, squared, always equals a minus b, squared, plus four "
               "times a b. No facts needed: expand both sides, and they match.",
    "substitute": "Step two is substitution. Our facts say a minus b is four, and a b is one. So we swap "
                  "them in.",
    "arithmetic": "Step three is arithmetic. Four squared, plus four times one, is twenty.",
    "chain": "Now read the whole chain, from the top left to the bottom right: a plus b, squared, equals "
             "twenty. And every link in the chain is either algebra, or substitution.",
    "outro": "That's a proof by calculation. In Lean, you'll write exactly this chain, and justify each "
             "link the same way.",
}

KNOWN_A = BLUE_C      # the fact a − b = 4 and everything it touches
KNOWN_B = YELLOW_C    # the fact ab = 1
ALGEBRA = TEAL_C
SUBST = GOLD_C


class CalcChain(NarratedScene):
    def construct(self):
        # --- the puzzle: two facts and a goal
        fact1 = MathTex("a-b", "=", "4")
        fact2 = MathTex("ab", "=", "1")
        fact1[0].set_color(KNOWN_A)
        fact2[0].set_color(KNOWN_B)
        facts = VGroup(fact1, fact2).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        facts_box = SurroundingRectangle(facts, color=GREY_B, buff=0.3, corner_radius=0.1)
        facts_label = Text("We know", font_size=26, color=GREY_B).next_to(facts_box, UP, buff=0.15)
        known = VGroup(facts_label, facts_box, facts).to_corner(UL, buff=0.6)
        goal = MathTex("(a+b)^2", "=", "\\,?").scale(1.3)

        with self.beat("puzzle") as beat:
            self.play(FadeIn(facts_label), Create(facts_box), run_time=beat.until("minus"))
            self.play(Write(fact1), run_time=beat.until("times") )
            self.play(Write(fact2), run_time=beat.until("What"))
            self.play(Write(goal), run_time=beat.until("squared"))
            self.play(Indicate(goal[2], color=WHITE))

        # --- the shortcut idea
        solve = Text("Solve for a and b first?", font_size=34, color=GREY_B).next_to(goal, DOWN, buff=0.9)
        idea = Text("Rewrite what you want in terms of what you know", font_size=34, color=WHITE)
        idea.next_to(goal, DOWN, buff=0.9)
        with self.beat("shortcut") as beat:
            self.play(FadeIn(solve, shift=UP * 0.2), run_time=beat.until("But"))
            cross = Cross(solve, stroke_color=RED_C)
            self.play(Create(cross), run_time=0.6)
            self.play(FadeOut(solve), FadeOut(cross), FadeIn(idea, shift=UP * 0.2),
                      run_time=beat.until("rewrite"))

        # --- build the chain, one link per step
        lhs = MathTex("(a+b)^2").scale(1.15)
        r1 = MathTex("=", "(a-b)^2", "+", "4", "ab").scale(1.15)
        r2 = MathTex("=", "4^2", "+", "4", "\\cdot", "1").scale(1.15)
        r3 = MathTex("=", "20").scale(1.15)
        r1[1].set_color(KNOWN_A)
        r1[4].set_color(KNOWN_B)
        r1.next_to(lhs, RIGHT, buff=0.2)
        r2.next_to(r1, DOWN, buff=0.45, aligned_edge=LEFT)
        r3.next_to(r2, DOWN, buff=0.45, aligned_edge=LEFT)
        chain = VGroup(lhs, r1, r2, r3).move_to(ORIGIN + DOWN * 0.3 + LEFT * 0.8)

        def tag(text, color, line):
            label = Text(text, font_size=28, color=color)
            label.next_to(line, RIGHT, buff=0.8)
            label.set_x(chain.get_right()[0] + 1.6)
            return label

        with self.beat("algebra") as beat:
            self.play(FadeOut(idea), ReplacementTransform(goal[0], lhs), FadeOut(goal[1:]),
                      run_time=beat.until("always"))
            self.play(Write(r1), run_time=beat.until("No"))
            expand = MathTex("a^2+2ab+b^2", color=GREY_A).scale(0.95).next_to(r1, UP, buff=0.4)
            both = VGroup(
                Arrow(lhs.get_top(), expand.get_left() + DOWN * 0.1, buff=0.1, color=GREY_B, stroke_width=3),
                Arrow(r1[1:].get_top(), expand.get_right() + DOWN * 0.1, buff=0.1, color=GREY_B, stroke_width=3),
            )
            t1 = tag("algebra", ALGEBRA, r1)
            self.play(GrowArrow(both[0]), GrowArrow(both[1]), FadeIn(expand), run_time=beat.until("match"))
            self.play(FadeIn(t1, shift=LEFT * 0.2))
        self.play(FadeOut(both), FadeOut(expand), run_time=0.4)

        with self.beat("substitute") as beat:
            t2 = tag("substitution", SUBST, r2)
            self.play(Indicate(fact1, color=KNOWN_A), Indicate(r1[1], color=KNOWN_A), run_time=beat.until("and"))
            self.play(Indicate(fact2, color=KNOWN_B), Indicate(r1[4], color=KNOWN_B), run_time=beat.until("So"))
            self.play(
                Write(r2[0]), TransformFromCopy(fact1[2], r2[1]), Write(r2[2]), Write(r2[3]), Write(r2[4]),
                TransformFromCopy(fact2[2], r2[5]),
                run_time=beat.until("swap") + 0.6,
            )
            self.play(FadeIn(t2, shift=LEFT * 0.2))

        with self.beat("arithmetic") as beat:
            t3 = tag("algebra", ALGEBRA, r3)
            self.play(Write(r3), run_time=beat.until("twenty"))
            self.play(FadeIn(t3, shift=LEFT * 0.2))

        with self.beat("chain") as beat:
            start = SurroundingRectangle(lhs, color=WHITE, buff=0.12)
            end = SurroundingRectangle(r3[1], color=WHITE, buff=0.12)
            path = CurvedArrow(start.get_bottom() + DOWN * 0.05, end.get_left() + LEFT * 0.05,
                               angle=TAU / 8, color=WHITE)
            self.play(Create(start), run_time=beat.until("bottom"))
            self.play(Create(path), Create(end), run_time=beat.until("And"))
            self.play(Indicate(t1, color=ALGEBRA), Indicate(t3, color=ALGEBRA), run_time=beat.until("or"))
            self.play(Indicate(t2, color=SUBST))

        with self.beat("outro") as beat:
            title = Text("Proof by calculation", font_size=44).to_edge(UP, buff=0.6)
            lean = [Text(s, font="Noto Sans Mono", font_size=26, color=c) for s, c in
                    (("by ring", ALGEBRA), ("by rw [h1, h2]", SUBST), ("by ring", ALGEBRA))]
            for label, old in zip(lean, (t1, t2, t3)):
                label.move_to(old, aligned_edge=LEFT)
            self.play(FadeOut(start), FadeOut(end), FadeOut(path), FadeOut(known), Write(title),
                      run_time=beat.until("Lean"))
            self.play(*(ReplacementTransform(old, new) for old, new in zip((t1, t2, t3), lean)),
                      run_time=beat.until("justify"))
        self.wait(0.8)
