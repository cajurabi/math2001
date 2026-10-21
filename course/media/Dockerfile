# Media pipeline image: Manim Community Edition + stable-ts forced alignment (CPU).
# Used only by course authors (course/media/build.sh), never by students.
FROM manimcommunity/manim:v0.22.0

USER root
# stable-ts shells out to ffmpeg to read audio (Manim itself uses PyAV's bundled libraries)
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*
# CPU-only torch first, so stable-ts doesn't pull in gigabytes of CUDA libraries
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch torchaudio \
    && pip install --no-cache-dir "stable-ts>=2.19"
USER manimuser
WORKDIR /work/course/media
ENTRYPOINT ["python", "-m", "pipeline.build"]
