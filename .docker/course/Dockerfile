# Local course image: Lean 4 toolchain + prebuilt math2001 project + the interactive course site.
# Replaces the Gitpod image (.gitpod.yml) for students running Docker locally:
#   docker compose up            → http://localhost:8080
# Targets:
#   lean-base  Lean + Mathlib + Library, built (also used by .devcontainer for VS Code)
#   runtime    lean-base + course site + websocket bridge (default for compose)

FROM node:24-bookworm AS lean-base

RUN apt-get update && apt-get install -y --no-install-recommends git curl ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

USER node
WORKDIR /home/node/math2001
ENV PATH="/home/node/.elan/bin:${PATH}"

# install elan, then the toolchain pinned by this repo (not upstream's main branch)
RUN curl -sSf https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh \
    | sh -s -- -y --default-toolchain none
COPY --chown=node:node lean-toolchain ./
RUN elan toolchain install "$(cat lean-toolchain)" && elan default "$(cat lean-toolchain)"

# fetch dependencies and the prebuilt Mathlib cache; fall back to compiling if the cache is gone
COPY --chown=node:node lakefile.lean lake-manifest.json ./
RUN (lake exe cache get || echo "WARNING: Mathlib cache unavailable, Mathlib will be compiled") \
    && rm -rf /home/node/.cache/mathlib

COPY --chown=node:node Library.lean ./
COPY --chown=node:node Library ./Library
RUN lake build Library AutograderLib

COPY --chown=node:node Math2001 ./Math2001
COPY --chown=node:node .vscode ./.vscode


FROM node:24-bookworm AS web-build

WORKDIR /src
COPY course/lean-editor/package.json course/lean-editor/package-lock.json course/lean-editor/
RUN cd course/lean-editor && npm ci --no-audit --no-fund
COPY course/site/package.json course/site/package-lock.json course/site/
RUN cd course/site && npm ci --no-audit --no-fund

# lessons pull the book's text (html/) and Lean files (Math2001/) at build time
COPY html ./html
COPY Math2001 ./Math2001
COPY course/assets.lock.json* course/
COPY course/lean-editor course/lean-editor
COPY course/site course/site
RUN cd course/lean-editor && npx vite build
# public/media holds explainer media synced from the asset cache on the build host, if any
RUN cd course/site && npm run build


FROM lean-base AS runtime

COPY --chown=node:node course/server/package.json course/server/package-lock.json /home/node/server/
RUN cd /home/node/server && npm ci --omit=dev --no-audit --no-fund
COPY --chown=node:node course/server/index.mjs /home/node/server/
COPY --from=web-build --chown=node:node /src/course/site/dist /home/node/site

ENV PORT=8080 \
    STATIC_DIR=/home/node/site \
    LEAN_PROJECT_DIR=/home/node/math2001
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s CMD curl -fsS http://localhost:8080/healthz || exit 1
CMD ["node", "/home/node/server/index.mjs"]
