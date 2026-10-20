---
title: Verifex
emoji: ⚖️
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 6.9.0
app_file: app.py
pinned: false
---

# Verifex - Deepfake Detector

Verifex is a deepfake detector that uses a trained **Xception** model plus a
three-tier forensic pipeline to classify images as **Real** or **Fake**.

## How a scan works

| Tier | What it checks | Behaviour |
| --- | --- | --- |
| **1a - Metadata** | EXIF / XMP / PNG text chunks for known generative-AI signatures | If an AI signature is found the image is marked **Fake** immediately (100%) |
| **1b - C2PA** | Cryptographic Content Credentials manifests (`c2pa-python`) | A manifest declaring AI generation marks the image **Fake** immediately (100%) |
| **2 - Pixel ensemble** | Xception + frequency + edge analysis | Runs only when Tier 1 finds nothing |

Ensemble scoring: `fake_p * 0.7 + frequency * 0.2 + edge * 0.1`, with a strict
**0.50** decision threshold. Score-CAM heatmaps are generated from the 16
highest-variance feature channels.

## Project structure

```
.
├── app.py                   Hugging Face Space entry point (boots app_server on 7860)
├── app_server.py            Serves the API and the static UI
├── backend/
│   └── xception_deepfake_detector.h5   Trained model (299x299x3, frozen base)
├── web/                     Static frontend (also deployed to Vercel)
│   ├── index.html           Landing page
│   ├── login.html / signup.html
│   ├── dashboard.html       Scan + history UI
│   ├── app.js               Frontend logic, API routing, sleep/wake handling
│   └── config.js            Sets window.__VERIFEX_API_BASE__ for production
├── convex/                  Convex schema + functions (scan history, users)
├── Dockerfile               Optional container image (port 7860)
├── docker-compose.yml       Optional local container run
└── requirements.txt         Pinned Python dependencies
```

## API

| Route | Method | Purpose |
| --- | --- | --- |
| `/health` | GET | Liveness probe - used by the frontend to detect a sleeping Space |
| `/predict` | POST | Image analysis (multipart `file` field) |
| `/api/*` | GET/POST | Scan history, account settings, Clerk sync |

All responses include permissive CORS headers so the Vercel-hosted frontend can
call this backend cross-origin.

## Local development

Windows (recommended wrapper):

```bash
cd "web app"
.\run_local.bat
```

Manual run:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app_server.py
```

The server starts on `http://localhost:8501` (override with the `PORT`
environment variable). The neural runtime is preloaded in a background thread,
so the port is reachable immediately while the model warms up.

## Deployment

- **Frontend:** Vercel, with the project root set to `web/`.
- **Backend:** Hugging Face Space, listening on port 7860.

The Space's `README.md` frontmatter deliberately keeps `sdk: gradio` (rather than
`sdk: docker`) because that Space's free `cpu-basic` allocation is tied to the
Gradio SDK. `app.py` therefore does not start a Gradio UI — it simply boots the
Verifex HTTP backend on port 7860.

Because free Spaces sleep when idle, the frontend pings `/health` before every
scan. If the backend is asleep it shows a notice and polls until the Space
wakes, then continues the scan automatically.

Set the deployed backend URL in `web/config.js` (`PRODUCTION_API_BASE`) so the
Vercel frontend knows where to send requests.

## Environment variables

Create a `.env.local` file (git-ignored):

```
CONVEX_URL=https://<your-deployment>.convex.cloud
CLERK_PUBLISHABLE_KEY=pk_test_...
```
