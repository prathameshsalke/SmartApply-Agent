# ClipForge

A local-first MVP for turning authorized video sources into short highlight clips. This project is added alongside the repository's existing SmartApply demo; it does not remove or change that application.

## What works

- Upload MP4, MOV, MKV, WEBM, and M4V files (up to 2 GB).
- Local speech transcription using Whisper, with no paid AI API.
- Rank transcript windows with a simple, transparent heuristic score (not a promise of virality or views).
- Review suggested timestamps and transcript context in a dark studio interface.
- Export a selected segment as vertical 9:16, square 1:1, or original-ratio MP4 using FFmpeg.
- Generate editable draft title, description, and tags from transcript text.
- Keep projects and exports on local disk; delete a project and its media via the API.

This MVP intentionally does not download videos from YouTube URLs, publish to social platforms, or provide face tracking/caption styling. Only process video you own or have permission to use. YouTube/API automation can be added later with the platform's official authorization flow.

## Requirements

- Python 3.10+
- FFmpeg and ffprobe available on PATH (install from [ffmpeg.org](https://ffmpeg.org/))
- CPU works for Whisper; processing can be slow. Whisper downloads its `base` model on first analysis. The model weights are not bundled in this repository.

## Run locally

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-clipforge.txt
python -m clipforge
```

Open http://127.0.0.1:8000. API docs are available at http://127.0.0.1:8000/docs.

For a lightweight API-only check without transcription installed:

```bash
uvicorn clipforge.api:app --reload
```

## API overview

- `GET /api/health`
- `GET /api/jobs`
- `POST /api/jobs?clip_limit=20` — multipart field `video`
- `GET /api/jobs/{job_id}` — poll processing status
- `POST /api/jobs/{job_id}/render` — JSON `{"clip_index":0,"layout":"vertical"}`
- `GET /api/exports/{filename}` — download rendered MP4
- `DELETE /api/jobs/{job_id}` — remove source and exports

Job records and media are stored under `data/clipforge/` and are excluded from Git. The MVP's JSON job store is intended for single-user local development, not concurrent production deployment. Do not expose it directly to the public internet; add authentication, quotas, isolated workers, durable database/object storage, and upload scanning before deployment.

## How suggestions work

Whisper segments are grouped into short windows. A heuristic score considers a few conversational hook words, punctuation, and transcript density. It is a basic sorting aid only—not a trained virality model. Results depend on the language and audio quality. Clips are ranked without overlap and then shown chronologically.

## Stack

FastAPI, Python, Whisper (optional local dependency), FFmpeg/ffprobe, and plain HTML/CSS/JavaScript. These tools are free/open-source software; compute, storage, electricity, and bandwidth may still have costs.

---

# SmartApply-Agent (original project)

The original job-application demo remains available as before. See the existing project documentation in the repository history or run its existing `app.main` and `app.api` entry points.
