# SmartApply-Agent

The existing SmartApply job-application automation demo is preserved. A separate local-first video clipping MVP, **ClipForge**, has been added alongside it.

- ClipForge guide: [CLIPFORGE_README.md](CLIPFORGE_README.md)
- Start ClipForge: `pip install -r requirements.txt && pip install -r requirements-clipforge.txt && python -m clipforge`
- Start the existing SmartApply demo: `python -m app.main`

ClipForge accepts local video uploads (not YouTube downloads), transcribes locally with Whisper, suggests timestamped highlights, and exports selected clips with FFmpeg. It is an MVP for local development; see its guide for setup, limitations, and safety notes.

## SmartApply-Agent

SmartApply-Agent is an AI-powered job application assistant demo. It analyzes job descriptions, compares candidate resumes using ATS-style scoring, selects a suitable resume, simulates form filling, and tracks sample results. The original implementation and usage are retained in the `app/` package.
