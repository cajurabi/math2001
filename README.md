# The Mechanics of Proof

This repository contains the Lean code for the book [The Mechanics of Proof](https://hrmacbeth.github.io/math2001), by [Heather Macbeth](https://faculty.fordham.edu/hmacbeth1), developed for the course Math 2001 at Fordham University.

The Lean files corresponding to each chapter of the book are in the folder [`Math2001`](https://github.com/hrmacbeth/math2001/tree/main/Math2001).

## Interactive course (this branch)

This branch adds an interactive, self-paced course built on the book, for high-school students. It has lesson pages that include the book's text, live Lean editors, guided hints and narrated explainers. Students run everything locally with Docker. No Gitpod account is needed.

```bash
git clone -b interactive-course https://github.com/cajurabi/math2001.git
cd math2001
docker compose up
```

Then open http://localhost:8080. The first run takes about 5–15 minutes while it downloads Lean and Mathlib. See [`course/PLAN.md`](course/PLAN.md) for the course plan and syllabus.

| Folder | What's in it |
|---|---|
| `course/site` | The course website (Astro + Starlight). Lessons are in `src/content/docs/`. |
| `course/lean-editor` | The `<lean-editor>` web component (lean4monaco + Lean infoview). |
| `course/server` | Serves the site and connects each browser editor to its own `lake serve`. |
| `course/media` | Authoring pipeline for narrated explainers (Manim + OpenRouter TTS). Its output is cached outside the repo. |
| `.docker/course` | The course image. The `.devcontainer` uses the same image for VS Code. |

To work in VS Code instead, install the Dev Containers extension, open this folder and choose **Reopen in Container**.

You can also [install Lean](https://leanprover-community.github.io/get_started.html) on your own computer, then clone this repository.
