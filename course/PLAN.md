# Interactive Course Plan — *The Mechanics of Proof* for High School

Branch: `interactive-course` · Status: **tooling decided (§6.3) — Week 1 Day 1 POC in progress**

## 1. Goals

| # | Goal | Notes |
|---|------|-------|
| 1 | Replace Gitpod with a **local Docker** environment for students | One `docker compose up` gives the course web app + a Lean server; VS Code Dev Container as the "power user" path. |
| 2 | Turn the book into an **interactive local web course** with 3Blue1Brown-style drill-down explainers | Students read on their own; explainers are optional "dig deeper" pop-outs (narrated animation + optional interactive widget). |
| 3 | An **11-week syllabus** covering ~80% of the book, where every lesson ends at a natural stopping point | §4. |
| 4 | Recreate the **11 homework sets** (HW0–HW10) and slot them into the syllabus | §5. |
| 5 | Target an **11th grader** with Algebra 1/2 + Trig, no Calculus II | §3. |
| 6 | Generated assets (audio, video, images) live **outside the repo**, keyed by content hash so rebuilds never pay to regenerate | §7. |

Deliverable order: this plan → tooling decision → POC of **Week 1, Day 1** → the rest of the course.

## 2. What the source material actually contains (findings)

These correct a few assumptions in the original brief, and they change the scope:

- **Your fork matches upstream exactly** (`e660f42`, Dec 2024). Lean is pinned to `leanprover/lean4:v4.3.0` with Mathlib `v4.3.0`, plus Duper and `lean4-autograder`.
- **`Math2001/` is not an answer key.** The chapter files contain the book's *worked examples* (already solved) plus the *exercises* (left as `sorry`, about 450 of them). Chapter 7 has no exercises.
- **`Math2001/Homework/` contains problem statements, not solutions.** Each `hwN.lean` is the formal statement of each problem (`theorem problemK … := by sorry`, tagged `@[autograded N]`). Upstream does not publish solutions.
- **The prose homework already exists.** The upstream wiki (`github.com/hrmacbeth/math2001/wiki/Homework-N`) has the English statement of every problem, with hints and special instructions (e.g. "Lean only", "don't use `exhaust`"). These are the Fall 2024 versions. So we don't need to reverse-engineer the questions. We do need to **write and verify our own reference solutions** (§5.3).
- **The instructor notes describe 13 weeks, not 11.** That was 2 × 75-minute classes per week, covering about 80% of the book, with 5–7 homework problems per week, oral Lean checks at weeks 5 and 10, and Lean-free written exams. Your 11-week target fits because there are exactly **11 homework sets (HW0–HW10)**: one per week.
- **The book assumes Calc II maturity but uses no calculus.** It says so in its introduction. The real prerequisite is fluent algebra: expanding and factoring, inequality manipulation, and substitution. An 11th grader can do this if we add algebra and notation scaffolding (§3).
- **Licensing:** the repo has no LICENSE file, and the Lean files carry "© Heather Macbeth, 2023. All rights reserved." See §9.

## 3. Audience adaptations (11th grade, pre-Calc II)

- **Reading load:** the book is about 83k words over 40 sections. We cap a lesson at roughly 1,500–2,500 words of reading plus 3–6 Lean exercises, which is about 45–60 minutes. Long sections (1.3, 1.4, 6.x, 8.1) are split.
- **Drill-down explainers** go where a high-schooler is likely to stall. For example:
  - Algebra: expanding `(a+b)²`, "substitute then simplify", why multiplying by a negative flips `≤`.
  - Number systems ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ, and why Lean cares which one you're in (subtraction in ℕ!).
  - Notation boot camp: ∀, ∃, ∧, ∨, ¬, →, ↔, set-builder notation, Σ / recursive sequences (before Ch 6), function notation and ℝ² (before Ch 8).
  - "For sufficiently large x": an informal, limit-free explanation (needed for HW5 #7 and HW7 #6).
- **Lean friction:** every lesson's first exercise is a guided one (fill in a blank or a single tactic), and only then a full proof.
- **Support model:** the instructor notes say most students needed office hours. For self-study we add hint ladders per exercise (hint 1 → hint 2 → worked step) and explainers that model *how to find* a proof, not only the proof itself.
- **Assessment:** keep the two "oral check" milestones as **Checkpoints** in weeks 5 and 10. Students solve unseen Lean problems and record or explain their reasoning to the instructor. Written exams are optional and up to the instructor.

## 4. Syllabus — 11 weeks, 4 days/week

Each week has **3 lesson days** and a **Lab day** (homework, plus a checkpoint in weeks 5 and 10). Homework on the Lab day of week *N* covers material already taught, usually that week and the end of the previous one.

| Wk | Day 1 | Day 2 | Day 3 | Lab day |
|----|-------|-------|-------|---------|
| 1 | **Setup + 1.1 Proving equalities + 1.2 …in Lean** | 1.3 Tips and tricks | 1.4 Proving inequalities (part 1) | **HW0** (1 problem, system check) |
| 2 | 1.4 Proving inequalities (part 2) | 1.5 A shortcut + 2.1 Intermediate steps | 2.2 Invoking lemmas | **HW1** (1.1–2.1) |
| 3 | 2.3 "Or" and proof by cases | 2.4 "And" | 2.5 Existence proofs | **HW2** (2.1–2.3) |
| 4 | 3.1 Definitions; parity | 3.2 Divisibility | 3.3 Modular arithmetic: theory | **HW3** (2.3–3.1) |
| 5 | 3.4 Modular arithmetic: calculations | 4.1 "For all" and implication | **Checkpoint 1** (Ch 1–3) | **HW4** (3.1–3.3) |
| 6 | 4.2 "If and only if" | 4.4 Contradictory hypotheses | 4.5 Proof by contradiction | **HW5** (3.4–4.1) |
| 7 | 5.1 Logical equivalence | 5.2 Law of the excluded middle | 5.3 Normal form for negations | **HW6** (4.2–5.1) |
| 8 | 6.1 Induction | 6.2 Recurrence relations | 6.3 Two-step induction | **HW7** (5.2–6.1) |
| 9 | 6.4 Strong induction | 8.1 Injectivity and surjectivity | 8.2 Bijectivity | **HW8** (6.2–6.4) |
| 10 | 8.3 Composition of functions | 8.4 Product types | **Checkpoint 2** (Ch 4–8) | **HW9** (8.1–8.4) |
| 11 | 9.1 Sets: introduction | 9.2 Set operations + 9.3 The type of sets | 10.1 Properties of relations | **HW10** (9.1–10.1) + wrap-up |

**Coverage:** 33 of 40 sections (82%). This matches the sections the Fall 2024 homework actually uses.

**Optional enrichment** (not scheduled; shipped as bonus lessons): 3.5 Bézout · 4.3 Unique existence · 6.5 Pascal's triangle · 6.6 Division algorithm · 6.7 Euclidean algorithm · Ch 7 Number theory (primes, √2) · 10.2 Equivalence relations.

**Stopping-point rule:** a lesson ends on a completed idea plus a finished exercise, never mid-example. Where a section is split (1.4), the split falls at a subsection boundary. The exact boundaries are chosen when we author each week.

## 5. Homework

### 5.1 Placement (from the problems' content)

| HW | Problems | Depends on | Lab |
|----|----------|-----------|-----|
| 0 | n ≥ 5 ⇒ n² > 2n+11 | 1.4 | W1 |
| 1 | Linear-equation and polynomial inequalities; #5 is `sq_le_sq` (Example 2.1.7, Lean-only) | 1.1–1.4, 2.1 | W2 |
| 2 | Cancel; `le_antisymm`; or-cases; `le_or_succ_le` | 2.1–2.3 | W3 |
| 3 | Or-introduction; quadratic roots; ∃ witnesses; odd cubes | 2.3–2.5, 3.1 | W4 |
| 4 | Parity; divisibility; `Int.not_dvd_of_exists_lt_and_lt`; mod rules from definitions | 3.1–3.3 | W5 |
| 5 | Mod calculations, x⁵ ≡ x; ∀/→; `interval_cases`; "sufficiently large" | 3.4, 4.1 | W6 |
| 6 | Non-existence by contradiction; ↔; logical equivalence (Lean-only) | 4.2, 4.4–4.5, 5.1 | W7 |
| 7 | `not_imp` from scratch with `by_cases`; `push_neg`; powers mod 7 by induction; Bernoulli | 5.2–5.3, 6.1 | W8 |
| 8 | Recurrences; two-step; strong induction (n = 2ᵃ·odd) | 6.2–6.4 | W9 |
| 9 | Prove-or-disprove injective/surjective/bijective, including on ℝ³ → ℝ² | 8.1–8.4 | W10 |
| 10 | Set ⊆ / =; finite sets by hand; relation properties (+ a directed-graph sketch on paper) | 9.1–9.3, 10.1 | W11 |

### 5.2 Student-facing format
- Each HW page in the web app shows the prose statement from the wiki (rewritten for 11th-grade reading level where needed) and a **"Write it in words"** box. It also has an embedded **Lean editor** pre-loaded with the `hwN.lean` statement, and the hints and special instructions.
- Students submit both the prose and the Lean versions, as in the original course. Lean is auto-checked locally (does it compile with no `sorry`?). Whether submissions go to a grader such as GitHub Classroom or Gradescope is out of scope for now.

### 5.3 Reference solutions (instructor-only)
- We write a Lean solution for every HW problem and every `sorry` exercise used in a lesson. Each solution must compile against the pinned toolchain; CI runs `lake build` on it.
- We also write a prose solution per HW problem, for instructors.
- **Solutions must not live in a public branch** (see open question Q4). Proposed: a private repo or a git submodule, mounted into the dev container only for instructors.

## 6. Tooling decisions (TO DECIDE)

Researched 2026-10-21. Versions are current as of that date.

### 6.1 Proposed architecture (Docker Compose)

```
┌─ course-site (nginx) ─────────────┐     ┌─ lean (Node bridge) ──────────────────┐
│ Astro + Starlight static build    │ ws  │ one `lake serve` per editor session,  │
│ MDX lessons, KaTeX                │◀───▶│ run in the prebuilt math2001 project  │
│ <LeanEditor> lean4monaco+infoview │     │ + leanprover-community/repl (warm)    │
│ <Explainer> video + JSXGraph      │     │   for "check my answer"               │
└───────────────────────────────────┘     └───────────────────────────────────────┘
        ▲ static media (from cache)
┌─ media pipeline (offline; authors only, never students) ──────────────────────┐
│ Manim CE 0.22 container + ElevenLabs TTS service + content-hash cache (§7)     │
└────────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Decisions

| # | Decision | Options | Recommendation |
|---|----------|---------|----------------|
| D1 | **Lean version** | **(a)** Stay on 4.3.0. Faithful to the book and the autograder, but today's editor tooling on 4.3 is unproven and the Mathlib 4.3 cache may be gone. **(b)** Base on a community port: `joewatt95/math2001` (Lean 4.33.1, PORTING.md, autograder attributes commented out) or `npflueger/math2001` (4.35.0). Modern tooling, but a third-party fork. | Run a **1-day spike** at the start of the POC: lean4monaco + infoview against 4.3.0 in Docker. If it works, stay on 4.3.0. If not, move to the 4.33 port. |
| D2 | **In-page Lean editor** | **(a)** lean4monaco + `@leanprover/infoview` in our own component, with a small websocket bridge or lean4web's server. **(b)** Embed a full lean4web instance in an iframe. **(c)** Read-only goal stepping via the REPL only. | **(a)**, with the REPL as a separate answer checker. Jupyter (`lean4_jupyter`) is too immature. Verso and in-browser WASM aren't viable on this Lean version. |
| D3 | **Site framework** | Astro 7 + Starlight + MDX · Docusaurus 3 · Quarto / MyST | **Astro + Starlight.** It's built on Vite, so lean4monaco's Vite setup carries over, and its React islands are a good fit for the editor and widgets. |
| D4 | **Explainers** | **(a)** Manim CE (pre-rendered narrated video) + JSXGraph (live interactive diagram). **(b)** Remotion: one React source for video and interactive (commercial license needed for organisations of more than 3 people). **(c)** Motion Canvas (stale) or Revideo. | **(a).** Manim is the actual 3b1b look. JSXGraph covers the "drag the slider" drill-downs. |
| D5 | **Text-to-speech** | **(a)** ElevenLabs API directly, using `/with-timestamps` for character-level alignment to sync animations (needs an ElevenLabs key/plan). **(b)** ElevenLabs through **OpenRouter** (`/api/v1/audio/speech`, live since 2026-10-07): one bill, but no timestamps and premade voices only. Timing would come from a separate alignment pass (Whisper, or OpenRouter `scribe-v2` if it returns word times). | **(a)** for narration that drives animation timing. (b) works if staying on one OpenRouter bill matters more; it costs one extra alignment step. |
| D6 | **Reference solutions location** | Private repo / submodule · encrypted file in this repo · outside git | **Private repo**, mounted into the container only for instructors. |

### 6.3 Decision log

| # | Status | Choice |
|---|--------|--------|
| D1 | ✅ decided | Spike 4.3.0 first; fall back to the Lean 4.33 port if the editor/infoview fails |
| D2 | ✅ decided | lean4monaco + infoview component, with the REPL as answer checker |
| D3 | ✅ decided | Astro + Starlight + MDX |
| D4 | ✅ decided | Manim CE videos + JSXGraph interactives |
| D5 | ✅ decided | ElevenLabs **via OpenRouter**, narration in per-beat chunks, plus a **local forced-alignment** pass for word timestamps (see 6.4) |
| D6 | ✅ decided | Separate private repo for reference solutions |

### 6.4 Text-to-speech with timestamps on OpenRouter

I checked all 36 OpenRouter speech models on 2026-10-21. OpenRouter's `/audio/speech` endpoint returns **only raw audio bytes (mp3/pcm)**, for every provider. **No OpenRouter TTS model returns timestamps**, whether ElevenLabs, MiniMax, Fish Audio, Gemini TTS, MAI-Voice, Deepgram or Kokoro. So the timestamps have to come from our side, and that turns out to be cheap and accurate:

1. **Chunk narration by beat.** Each animation beat, usually one sentence, is its own TTS call. The audio length *is* the beat duration, which covers about 90% of 3b1b-style syncing (`self.play(..., run_time=beat.duration)`). It also keeps cache invalidation per sentence (§7).
2. **Forced alignment for in-sentence cues.** We already know the exact script text, so we *align* rather than transcribe. A local aligner (stable-ts / WhisperX alignment, or aeneas) runs in the media container and gives word start/end times accurate to tens of milliseconds. It's free, offline, and its output is cached by audio hash.
3. Script markup such as `Notice <cue:highlight/>this term…` maps a cue to the next word's aligned start time.

Result: ElevenLabs voice quality on your existing OpenRouter account, with timestamps as good as ElevenLabs' `/with-timestamps`. The only extra is the alignment step, which is local and free. Cost estimate: Day 1 has about 3k characters of narration, roughly $0.24 at Eleven v4 list price ($80 per million characters). Cheaper voices on OpenRouter worth an A/B listen: Eleven v4 Turbo ($40/M), MAI-Voice-2.1 (~$22/M), Fish Audio S2.1 Pro (~$15/M).

`manim-voiceover` 0.4.0 already hashes the text, voice and model into its cache, but its ElevenLabs plugin is outdated (SDK < 0.3). We'd write a small custom `SpeechService` that calls the API with timestamps and stores results in the §7 cache.

## 7. Generated-asset cache (content-addressed, outside the repo)

- **Store:** `~/.cache/math2001-course/` by default, overridable with `COURSE_ASSET_CACHE`. Optionally sync it to a bucket (S3, R2 or similar) so several instructors share one cache.
- **Key:** `sha256(generator-id + generator-version + canonical JSON of all inputs)`. Inputs include, for example, narration text, voice ID, TTS model and settings for audio, or the scene source hash plus the hashes of its audio dependencies for video.
- **Repo holds only a manifest** (`course/assets.lock.json`) mapping each logical asset (`w01d1/explainer-calc-chain/narration`) to its key. A build does this:
  1. Compute the expected key.
  2. If the key is in the cache, use it.
  3. If not, regenerate it, which costs API tokens or credits.
  4. Update the lock file.
- A `--dry-run` mode reports what would be regenerated, and its estimated character or credit cost, before anything is spent.
- A change to a narration line invalidates only that line's audio and the video segments that depend on it, not the whole lesson. This is why narration is chunked per sentence or beat.

## 8. Week 1 Day 1 POC — scope

1. **Docker:** `docker compose up` starts the course app at `http://localhost:<port>` plus a Lean server with the pinned toolchain and the Mathlib cache built into the image.
2. **Lesson page** for 1.1 + 1.2:
   - Original prose written for 11th graders, following the book's examples.
   - KaTeX math.
   - Calculation chains shown step by step.
3. **Two drill-down explainers:**
   - (a) "What a proof by calculation is": a narrated animation of the `(a+b)² = (a−b)² + 4ab` chain.
   - (b) "Reading a Lean `calc` block": goal state ↔ prose, side by side.
   - Both are narrated with ElevenLabs and cached through §7.
4. **Embedded Lean exercises** from `01_Proofs_by_Calculation/02_Proving_Equalities_in_Lean.lean`, with a live goal view and a pass/fail check.
5. **Setup checklist page** that replaces the Gitpod instructions in the README.

POC exit criteria:
- A fresh machine goes from clone to solving the first exercise in the browser in **15 minutes or less** (excluding the image download).
- A second `build` makes **zero** TTS/render calls.

## 9. Risks and open questions

| Risk | Mitigation |
|------|-----------|
| **Copyright/licensing**: the book text and Lean files are "All rights reserved" with no LICENSE. | Write original lesson prose (no copying of the book's text), link to the book's sections, and use the repo's Lean files as students already do. **Recommend contacting Dr. Macbeth before distributing beyond your own classroom.** |
| Lean 4.3.0 / Mathlib (Nov 2023) is old. Newer editor tooling may not support it, and the Mathlib cache download for that old commit may no longer be hosted. | Bake the Mathlib build into the Docker image once and publish the image. Verify in the POC. |
| Docker image size (Mathlib oleans are several GB). | Prebuilt multi-arch image (amd64 + arm64; Lean 4.3.0 ships `linux_aarch64`) on GHCR, so students pull it once. |
| Student laptops (Chromebooks can't run Docker). | Fallback: a hosted instance of the same container. Out of scope for the POC. |
| TTS/render cost creep | §7 cache plus `--dry-run` cost estimate. |
