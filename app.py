"""Hugging Face Space entry point for the Verifex inference backend.

Hugging Face runs `python app.py` for this Space and proxies external traffic to
port 7860. Rather than starting a Gradio UI, this entry point boots the real
Verifex backend (the standard-library HTTP server in app_server.py) so that the
frontend, the `/predict` endpoint, the `/health` probe and the `/api/*` routes
all live on a single origin.

The Space intentionally keeps `sdk: gradio` in README.md: this Space's free
runtime allocation is tied to that SDK, so the frontmatter is left untouched and
only the code is swapped.

The Dockerfile does not use this file (its CMD runs app_server.py directly); it
exists for the Hugging Face Gradio-SDK runtime.
"""

import os
import sys

# Make sibling modules (app_server) importable no matter where the process starts.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Hugging Face routes traffic to 7860. Respect an explicit PORT if one is set.
os.environ.setdefault("PORT", "7860")

from app_server import main  # noqa: E402

if __name__ == "__main__":
    main()
