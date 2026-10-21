"""Media pipeline for course explainers: narration (TTS), alignment, Manim rendering, captions.

Everything expensive is content-addressed in the asset cache (outside the repo), so a rebuild
only regenerates what actually changed.
"""

PIPELINE_VERSION = 1
