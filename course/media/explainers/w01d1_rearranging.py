"""Week 1 Day 1 explainer: what a "purely algebraic rearrangement" is (Examples 1.1.1 and 1.1.2).

Shows the moves the author uses: adding zero and regrouping (r = (r + 2s) − 2s), and expanding and
collecting like terms ((a + b)² = (a − b)² + 4ab), with the "try any numbers" test and the
contrast with substitution. History (al-Khwārizmī, al-jabr) is from MacTutor.

Every algebra and arithmetic step is shown on screen (see CLAUDE.md: never hide steps).
All equations here are checked with Lean (ring / numbers) before rendering.
"""

import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline.narration import NarratedScene  # noqa: E402

EXPLAINER = {"id": "w01d1/rearranging", "title": "What is an algebraic rearrangement?", "scene": "Rearranging"}

NARRATION = {
    "intro": "In Examples 1.1.1 and 1.1.2, the book calls some steps purely algebraic rearrangements. Here's "
             "what that means, and the exact moves the author used.",
    "history": "Rearranging is as old as algebra. In the 800s, al-Khwarizmi, a scholar at the House of Wisdom "
               "in Baghdad, wrote a book called al-jabr wa al-muqabala. Al-jabr means completion, and "
               "al-muqabala means balancing. The first word of that title became our word algebra.",
    "define": "A rearrangement rewrites an expression in a different form that is equal for every possible "
              "value of its letters. It uses only the rules of algebra, never the facts of the problem. That "
              "gives a simple test: plug in any numbers you like, and both sides must agree.",
    "moves": "These two examples use four kinds of moves. Adding zero. Regrouping brackets. Expanding "
             "products. And collecting like terms.",
    "ex2_goal": "Example 1.1.2 first. The facts are r plus two s equals negative one, and s equals three. The "
                "goal is r equals negative seven. The goal is about r alone, but the useful fact is about r "
                "plus two s. So the plan is to make r plus two s appear.",
    "ex2_zero": "Move one: add zero. Adding zero never changes a number, so r equals r plus zero. Now write "
                "the zero as two s minus two s, since anything minus itself is zero. Why two s? Because the "
                "fact has a plus two s in it. Add exactly the piece that's missing, and take it away again.",
    "ex2_regroup": "Move two: regroup. Adding two s minus two s to r is the same as first adding two s to r, "
                   "and then subtracting two s. Moving the brackets like this doesn't change the value. And now "
                   "r plus two s sits right there, in brackets.",
    "ex2_test": "Test it with any numbers. Take r equals five and s equals one. The left side is five. The right "
                "side is five plus two, minus two: seven minus two, which is five. It works for every r and s, "
                "so no facts were used.",
    "ex2_rest": "The next two steps are substitutions, and they do use the facts. Swap r plus two s for "
                "negative one, then swap s for three. The last step is arithmetic: two times three is six, and "
                "negative one minus six is negative seven.",
    "ex1": "Now Example 1.1.1. Its first line, a plus b squared equals a minus b squared plus four a b, uses "
           "the other two moves: expanding products, and collecting like terms.",
    "ex1_left": "Expand the left side. a plus b squared means a plus b, times a plus b. Multiply every term by "
                "every term: a times a, a times b, b times a, and b times b. That's a squared, plus a b, plus a "
                "b, plus b squared, because b times a is the same as a b. Collect the like terms: a b plus a b "
                "is two a b.",
    "ex1_right": "Now the right side. Expand a minus b, times a minus b, the same way. Watch the signs: minus b "
                 "times minus b is plus b squared. That gives a squared, minus a b, minus a b, plus b squared, "
                 "plus four a b. Collect the a b terms: negative a b, minus a b, plus four a b, is two a b.",
    "ex1_same": "Both sides come out to a squared plus two a b plus b squared, for every a and b. So the first "
                "line is a rearrangement: no facts used. The next line substitutes the facts. The last is "
                "arithmetic: four squared is sixteen, four times one is four, and sixteen plus four is twenty.",
    "summary": "So a rearrangement changes how an expression looks, never its value, and never uses the facts. "
               "Example 1.1.2 used adding zero and regrouping. Example 1.1.1 used expanding and collecting like "
               "terms. In Lean, ring checks rearrangements like these, and rw does the substitutions.",
}

ALG = TEAL_C        # rearrangement steps
SUBST = GOLD_C      # substitution steps
FACT_A = BLUE_C
FACT_B = YELLOW_C
ZERO = GREY_B
NOTE = GREY_B


def chain(rows, scale=0.8, buff=0.3):
    """Equation rows with their "=" signs lined up.

    rows: list of (eq_index, [(tex, color), ...]); eq_index is the position of the "=" part.
    """
    mobs = []
    for eq_index, parts in rows:
        tex = MathTex(*(t for t, _ in parts)).scale(scale)
        for part, (_, color) in zip(tex, parts):
            part.set_color(color)
        tex.eq_index = eq_index
        mobs.append(tex)
    group = VGroup(*mobs).arrange(DOWN, buff=buff)
    x = mobs[0][mobs[0].eq_index].get_center()[0]
    for tex in mobs[1:]:
        tex.shift(RIGHT * (x - tex[tex.eq_index].get_center()[0]))
    return group


def tags(rows, labels, x):
    """A label to the right of each chain row, all starting at the same x."""
    group = VGroup()
    for row, (text, color) in zip(rows, labels):
        label = Text(text, font_size=22, color=color)
        label.move_to([x, row.get_y(), 0], aligned_edge=LEFT)
        group.add(label)
    return group


class Rearranging(NarratedScene):
    def show(self, beat, word, *animations, occurrence=1, run_time=0.9):
        """Play `animations` briskly, then hold until `word` is spoken."""
        self.play(*animations, run_time=min(run_time, beat.until(word, occurrence)))
        rest = beat.until(word, occurrence, minimum=0.0)
        if rest > 0.02:
            self.wait(rest)

    def construct(self):
        # ---- what the book says
        title = Text("What is an algebraic rearrangement?", font_size=40).to_edge(UP, buff=0.7)
        quote = Text("“a purely algebraic rearrangement”", font_size=30, slant=ITALIC, color=ALG)
        source = Text("Examples 1.1.1 and 1.1.2", font_size=24, color=NOTE).next_to(quote, DOWN, buff=0.35)

        with self.beat("intro") as beat:
            self.show(beat, "book", FadeIn(title, shift=DOWN * 0.2))
            self.show(beat, "Here's", FadeIn(quote), FadeIn(source))
        self.play(FadeOut(VGroup(quote, source)), run_time=0.5)

        # ---- where the word comes from (MacTutor: al-Khwarizmi)
        who = Text("al-Khwārizmī (c. 780 – c. 850)", font_size=32).move_to(UP * 1.6)
        where = Text("House of Wisdom, Baghdad", font_size=24, color=NOTE).next_to(who, DOWN, buff=0.2)
        book = Text("Hisāb al-jabr wa'l-muqābala", font_size=30, slant=ITALIC).move_to(DOWN * 0.1)
        meanings = VGroup(
            Text("al-jabr = completion", font_size=26, color=ALG),
            Text("al-muqābala = balancing", font_size=26, color=ALG),
        ).arrange(RIGHT, buff=1.0).next_to(book, DOWN, buff=0.45)
        word = Text("al-jabr  →  algebra", font_size=34, color=YELLOW_C).next_to(meanings, DOWN, buff=0.6)

        with self.beat("history") as beat:
            self.show(beat, "wrote", FadeIn(who), FadeIn(where))
            self.show(beat, "Al-jabr", FadeIn(book))
            self.show(beat, "The", FadeIn(meanings[0]), occurrence=3)
            self.play(FadeIn(meanings[1]))
            self.show(beat, "algebra", FadeIn(word, shift=UP * 0.2), occurrence=2)
        self.play(FadeOut(VGroup(who, where, book, meanings, word)), run_time=0.5)

        # ---- the definition, and the test
        rule1 = Text("A rearrangement: the same value for every value of the letters", font_size=28)
        rule2 = Text("uses only the rules of algebra, never the problem's facts", font_size=26, color=NOTE)
        rule3 = Text("Test: try any numbers. Both sides must agree.", font_size=28, color=ALG)
        rules = VGroup(rule1, rule2, rule3).arrange(DOWN, buff=0.45).move_to(DOWN * 0.2)

        with self.beat("define") as beat:
            self.show(beat, "It", FadeIn(rule1))
            self.show(beat, "That", FadeIn(rule2), occurrence=2)
            self.play(FadeIn(rule3))
        self.play(FadeOut(rules), run_time=0.5)

        # ---- the four moves, each with a tiny example
        move_rows = VGroup(*(
            VGroup(Text(name, font_size=28, color=ALG), MathTex(example).scale(0.8)).arrange(RIGHT, buff=0.6)
            for name, example in (
                ("adding zero", "x = x + (y - y)"),
                ("regrouping", "x + (y - z) = (x + y) - z"),
                ("expanding", "2(x + 3) = 2x + 6"),
                ("collecting like terms", "3x + 5x = 8x"),
            )
        )).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(DOWN * 0.2)

        with self.beat("moves") as beat:
            self.wait(beat.until("Adding"))
            self.show(beat, "Regrouping", FadeIn(move_rows[0]))
            self.show(beat, "Expanding", FadeIn(move_rows[1]))
            self.show(beat, "And", FadeIn(move_rows[2]))
            self.play(FadeIn(move_rows[3]))
        self.wait(2.5)  # time to read all four before they go
        self.play(FadeOut(VGroup(title, move_rows)), run_time=0.5)

        # ---- Example 1.1.2: facts and goal
        fa = MathTex("r+2s", "=", "-1")
        fb = MathTex("s", "=", "3")
        fa[0].set_color(FACT_A)
        fb[0].set_color(FACT_B)
        facts = VGroup(fa, fb).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        box = SurroundingRectangle(facts, color=GREY_B, buff=0.25, corner_radius=0.1)
        label = Text("Facts", font_size=26, color=GREY_B).next_to(box, UP, buff=0.15)
        known = VGroup(label, box, facts).to_corner(UL, buff=0.6)
        ex_label = Text("Example 1.1.2", font_size=28, color=NOTE).to_edge(UP, buff=0.5)
        goal = MathTex("r", "=", "-7", "\\;?").scale(1.2).to_corner(UR, buff=0.9)

        with self.beat("ex2_goal") as beat:
            self.show(beat, "The", FadeIn(ex_label), FadeIn(label), Create(box), Write(facts), occurrence=2, run_time=1.5)
            self.show(beat, "The", Write(goal), occurrence=3)
            self.show(beat, "So", Indicate(goal[0]), Indicate(fa[0], color=FACT_A), run_time=1.5)

        r1 = chain([
            (1, [("r", WHITE), ("=", WHITE), ("r", WHITE), ("+", WHITE), ("0", ZERO)]),
            (0, [("=", WHITE), ("r", WHITE), ("+", WHITE), ("(2s-2s)", ZERO)]),
            (0, [("=", WHITE), ("(r+2s)", FACT_A), ("-", WHITE), ("2s", WHITE)]),
        ], scale=1.0, buff=0.4).move_to(LEFT * 1.5 + DOWN * 0.2)
        r1_tags = tags(r1, [("adding zero", ALG), ("0 = 2s − 2s", ALG), ("regrouping", ALG)], r1.get_right()[0] + 1.0)

        with self.beat("ex2_zero") as beat:
            self.show(beat, "so", Write(r1[0]))
            self.show(beat, "Now", FadeIn(r1_tags[0]))
            self.show(beat, "since", Write(r1[1]))
            self.show(beat, "Why", FadeIn(r1_tags[1]))
            self.show(beat, "Add", Indicate(fa[0][2:], color=FACT_A), Indicate(r1[1][3], color=ZERO), occurrence=2, run_time=1.5)

        with self.beat("ex2_regroup") as beat:
            self.show(beat, "Moving", Write(r1[2]), run_time=1.5)
            self.show(beat, "And", FadeIn(r1_tags[2]), occurrence=2)
            self.play(Indicate(r1[2][1], color=FACT_A), Indicate(fa[0], color=FACT_A))

        test = chain([
            (1, [("\\text{left: } r", WHITE), ("=", WHITE), ("5", GREEN_C)]),
            (1, [("\\text{right: } (r+2s)-2s", WHITE), ("=", WHITE), ("(5+2\\cdot 1)-2\\cdot 1", WHITE)]),
            (0, [("=", WHITE), ("(5+2)-2", WHITE)]),
            (0, [("=", WHITE), ("7-2", WHITE)]),
            (0, [("=", WHITE), ("5", GREEN_C)]),
        ], scale=0.75, buff=0.25).move_to(RIGHT * 3.2 + DOWN * 0.6)
        pick = MathTex("r = 5,\\; s = 1", color=NOTE).scale(0.75).next_to(test, UP, buff=0.35)

        with self.beat("ex2_test") as beat:
            self.show(beat, "Take", FadeOut(r1_tags), r1.animate.scale(0.8).to_edge(LEFT, buff=0.8))
            self.show(beat, "The", FadeIn(pick))
            self.show(beat, "The", Write(test[0]), occurrence=2)
            self.play(Write(test[1]), run_time=beat.until("seven"))
            self.play(Write(test[2]), run_time=beat.until("which"))
            self.play(Write(test[3]), Write(test[4]), run_time=beat.until("It", 2))
            self.play(Indicate(test[0][2], color=GREEN_C), Indicate(test[4][1], color=GREEN_C))
        self.play(FadeOut(VGroup(test, pick)), run_time=0.5)

        full = chain([
            (1, [("r", WHITE), ("=", WHITE), ("(r+2s)-2s", WHITE)]),
            (0, [("=", WHITE), ("-1-2s", WHITE)]),
            (0, [("=", WHITE), ("-1-2\\cdot 3", WHITE)]),
            (0, [("=", WHITE), ("-1-6", WHITE)]),
            (0, [("=", WHITE), ("-7", GREEN_C)]),
        ], scale=0.95, buff=0.32).move_to(LEFT * 1.6 + DOWN * 0.4)
        full_tags = tags(full, [("rearrangement", ALG), ("substitution: r + 2s = −1", SUBST),
                                ("substitution: s = 3", SUBST), ("arithmetic: 2 · 3 = 6", ALG),
                                ("arithmetic: −1 − 6 = −7", ALG)], full.get_right()[0] + 0.8)

        with self.beat("ex2_rest") as beat:
            self.show(beat, "Swap", ReplacementTransform(r1, full[0]), FadeIn(full_tags[0]), run_time=1.2)
            self.show(beat, "then", Write(full[1]), FadeIn(full_tags[1]), Indicate(fa, color=FACT_A))
            self.show(beat, "The", Write(full[2]), FadeIn(full_tags[2]), Indicate(fb, color=FACT_B), occurrence=3)
            self.show(beat, "and", Write(full[3]), FadeIn(full_tags[3]), occurrence=2)
            self.play(Write(full[4]), FadeIn(full_tags[4]), run_time=1.2)
            done = MathTex("r", "=", "-7", color=GREEN_C).scale(1.2).move_to(goal[:3])
            self.play(FadeOut(goal), FadeIn(done))
        self.play(FadeOut(VGroup(known, full, full_tags, done, ex_label)), run_time=0.6)

        # ---- Example 1.1.1: expanding and collecting
        ex1_label = Text("Example 1.1.1", font_size=28, color=NOTE).to_edge(UP, buff=0.5)
        first = MathTex("(a+b)^2", "=", "(a-b)^2+4ab").scale(1.1).next_to(ex1_label, DOWN, buff=0.4)
        first_tag = Text("expanding + collecting like terms", font_size=24, color=ALG).next_to(first, DOWN, buff=0.25)

        with self.beat("ex1") as beat:
            self.show(beat, "Its", FadeIn(ex1_label))
            self.show(beat, "uses", Write(first), run_time=1.5)
            self.play(FadeIn(first_tag))

        left = chain([
            (1, [("(a+b)^2", WHITE), ("=", WHITE), ("(a+b)(a+b)", WHITE)]),
            (0, [("=", WHITE), ("a\\cdot a", WHITE), ("+", WHITE), ("a\\cdot b", FACT_A), ("+", WHITE), ("b\\cdot a", FACT_A),
                 ("+", WHITE), ("b\\cdot b", WHITE)]),
            (0, [("=", WHITE), ("a^2", WHITE), ("+", WHITE), ("ab", FACT_A), ("+", WHITE), ("ab", FACT_A), ("+", WHITE), ("b^2", WHITE)]),
            (0, [("=", WHITE), ("a^2", WHITE), ("+", WHITE), ("2ab", FACT_A), ("+", WHITE), ("b^2", WHITE)]),
        ], scale=0.85, buff=0.32).move_to(DOWN * 1.0).to_edge(LEFT, buff=0.9)
        left_tags = tags(left, [("", ALG), ("expanding: each term × each term", ALG),
                                ("b · a = ab", ALG), ("collecting: ab + ab = 2ab", ALG)], left.get_right()[0] + 0.5)

        with self.beat("ex1_left") as beat:
            self.show(beat, "Multiply", FadeOut(first_tag), first.animate.scale(0.75).next_to(ex1_label, DOWN, buff=0.2),
                      Write(left[0]))
            self.show(beat, "That's", Write(left[1]), FadeIn(left_tags[1]), run_time=1.5)
            self.show(beat, "Collect", Write(left[2]), FadeIn(left_tags[2]), run_time=1.5)
            self.play(Write(left[3]), FadeIn(left_tags[3]), run_time=1.2)
        sum_left = MathTex("\\text{left: }", "a^2+2ab+b^2").scale(0.65).to_corner(UL, buff=0.4)
        sum_left[1].set_color(GREEN_C)
        self.play(FadeOut(VGroup(left[:3], left_tags)), ReplacementTransform(left[3], sum_left), run_time=0.7)

        right = chain([
            (1, [("(a-b)^2+4ab", WHITE), ("=", WHITE), ("(a-b)(a-b)+4ab", WHITE)]),
            (0, [("=", WHITE), ("a\\cdot a", WHITE), ("-", WHITE), ("a\\cdot b", FACT_A), ("-", WHITE), ("b\\cdot a", FACT_A),
                 ("+", WHITE), ("(-b)(-b)", FACT_B), ("+4ab", FACT_A)]),
            (0, [("=", WHITE), ("a^2", WHITE), ("-", WHITE), ("ab", FACT_A), ("-", WHITE), ("ab", FACT_A), ("+", WHITE), ("b^2", FACT_B),
                 ("+4ab", FACT_A)]),
            (0, [("=", WHITE), ("a^2", WHITE), ("+", WHITE), ("(-ab-ab+4ab)", FACT_A), ("+", WHITE), ("b^2", WHITE)]),
            (0, [("=", WHITE), ("a^2", WHITE), ("+", WHITE), ("2ab", FACT_A), ("+", WHITE), ("b^2", WHITE)]),
        ], scale=0.78, buff=0.3).move_to(DOWN * 1.05).to_edge(LEFT, buff=0.6)
        right_tags = tags(right, [("", ALG), ("expanding", ALG), ("(−b)(−b) = +b²", FACT_B),
                                  ("collecting ab terms", ALG), ("−1 − 1 + 4 = 2", ALG)], right.get_right()[0] + 0.4)

        with self.beat("ex1_right") as beat:
            self.show(beat, "Watch", Write(right[0]), run_time=1.2)
            self.show(beat, "That", Write(right[1]), FadeIn(right_tags[1]), run_time=1.5)
            self.show(beat, "Collect", Write(right[2]), FadeIn(right_tags[2]), run_time=1.5)
            self.show(beat, "is", Write(right[3]), FadeIn(right_tags[3]), occurrence=2, run_time=1.5)
            self.play(Write(right[4]), FadeIn(right_tags[4]), run_time=1.2)
        sum_right = MathTex("\\text{right: }", "a^2+2ab+b^2").scale(0.65).next_to(sum_left, DOWN, buff=0.2, aligned_edge=LEFT)
        sum_right[1].set_color(GREEN_C)
        self.play(FadeOut(VGroup(right[:4], right_tags)), ReplacementTransform(right[4], sum_right), run_time=0.7)

        proof = chain([
            (1, [("(a+b)^2", WHITE), ("=", WHITE), ("(a-b)^2+4ab", WHITE)]),
            (0, [("=", WHITE), ("4^2+4\\cdot 1", WHITE)]),
            (0, [("=", WHITE), ("16+4", WHITE)]),
            (0, [("=", WHITE), ("20", GREEN_C)]),
        ], scale=0.95, buff=0.32).move_to(LEFT * 1.4 + DOWN * 0.6)
        proof_tags = tags(proof, [("rearrangement: expand, collect", ALG), ("substitution: a − b = 4, ab = 1", SUBST),
                                  ("arithmetic: 4² = 16, 4 · 1 = 4", ALG), ("arithmetic: 16 + 4 = 20", ALG)],
                          proof.get_right()[0] + 0.6)

        with self.beat("ex1_same") as beat:
            self.show(beat, "So", Indicate(sum_left[1], color=GREEN_C), Indicate(sum_right[1], color=GREEN_C), run_time=1.5)
            self.show(beat, "The", ReplacementTransform(first, proof[0]), FadeIn(proof_tags[0]), occurrence=1, run_time=1.2)
            self.show(beat, "The", Write(proof[1]), FadeIn(proof_tags[1]), occurrence=2)
            self.show(beat, "and", Write(proof[2]), FadeIn(proof_tags[2]), occurrence=2)
            self.play(Write(proof[3]), FadeIn(proof_tags[3]), run_time=1.2)
        self.play(FadeOut(VGroup(ex1_label, sum_left, sum_right, proof, proof_tags)), run_time=0.6)

        # ---- summary
        heading = Text("Rearrangement", font_size=36, color=ALG).to_edge(UP, buff=0.7)
        lines = VGroup(
            Text("changes how an expression looks, never its value; uses no facts", font_size=26),
            VGroup(Text("Example 1.1.2:", font_size=26, color=NOTE), Text("adding zero, regrouping", font_size=26, color=ALG)).arrange(RIGHT, buff=0.3),
            VGroup(Text("Example 1.1.1:", font_size=26, color=NOTE), Text("expanding, collecting like terms", font_size=26, color=ALG)).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.4)
        lean = VGroup(
            VGroup(Text("by ring", font="Noto Sans Mono", font_size=30, color=ALG), Text("checks a rearrangement", font_size=24, color=NOTE)).arrange(RIGHT, buff=0.4),
            VGroup(Text("by rw [h]", font="Noto Sans Mono", font_size=30, color=SUBST), Text("substitutes a fact", font_size=24, color=NOTE)).arrange(RIGHT, buff=0.4),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(DOWN * 2.1)

        with self.beat("summary") as beat:
            self.show(beat, "Example", FadeIn(heading), FadeIn(lines[0]))
            self.show(beat, "Example", FadeIn(lines[1]), occurrence=2)
            self.show(beat, "In", FadeIn(lines[2]))
            self.play(FadeIn(lean, shift=UP * 0.2))
        self.wait(0.8)
