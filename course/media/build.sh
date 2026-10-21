#!/usr/bin/env bash
# Build the course explainers (narration + Manim videos) into the asset cache, then sync them
# into the site. Generated media never enters the repo; only course/assets.lock.json changes.
#
#   course/media/build.sh --dry-run        what would be generated, and its estimated cost
#   course/media/build.sh                  build everything that's missing
#   course/media/build.sh --only w01d1/calc-chain --quality draft
#
# Needs OPENROUTER_KEY in the repo's .env.local (only when narration must be synthesized).
set -euo pipefail

repo="$(cd "$(dirname "$0")/../.." && pwd)"
cache="${COURSE_ASSET_CACHE:-$HOME/.cache/math2001-course}"
mkdir -p "$cache"

docker build -q -t math2001-media:latest "$repo/course/media" >/dev/null

env_args=()
[[ -f "$repo/.env.local" ]] && env_args+=(--env-file "$repo/.env.local")

docker run --rm \
  "${env_args[@]}" \
  -e COURSE_ASSET_CACHE=/cache \
  -v "$repo:/work" \
  -v "$cache:/cache" \
  math2001-media:latest "$@"

if [[ " $* " != *" --dry-run "* ]]; then
  (cd "$repo/course/site" && node scripts/sync-media.mjs)
fi
