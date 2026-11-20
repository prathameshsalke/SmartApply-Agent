from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .analysis import MediaError, make_metadata, probe_duration, suggest_clips, transcribe
from .render import render_clip
from .storage import ALLOWED_SUFFIXES, EXPORT_DIR, JOBS_FILE, MAX_UPLOAD_BYTES, UPLOAD_DIR, new_id, read_jobs, safe_name, write_jobs

app = FastAPI(title="ClipForge", description="Local-first video highlight clipping MVP", version="0.1.0")
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")


class RenderRequest(BaseModel):
    clip_index: int = Field(ge=0)
    layout: str = Field(default="vertical", pattern="^(vertical|square|original)$")


def _get_job(job_id: str) -> dict[str, Any]:
    job = read_jobs().get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Project not found.")
    return job


async def _analyze(job_id: str) -> None:
    jobs = read_jobs()
    job = jobs.get(job_id)
    if not job:
        return
    job["status"] = "analyzing"
    write_jobs(jobs)
    try:
        source = UPLOAD_DIR / job["filename"]
        duration = await asyncio.to_thread(probe_duration, source)
        segments = await asyncio.to_thread(transcribe, source)
        clips = suggest_clips(segments, duration, job.get("clip_limit", 20))
        job.update({"status": "ready", "duration": duration, "segments": segments, "clips": clips, "metadata": make_metadata(" ".join(s["text"] for s in segments)), "error": None})
    except Exception as exc:
        job.update({"status": "error", "error": str(exc)})
    jobs[job_id] = job
    write_jobs(jobs)


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return (Path(__file__).parent / "static" / "index.html").read_text(encoding="utf-8")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ClipForge"}


@app.get("/api/jobs")
def list_jobs() -> list[dict[str, Any]]:
    return sorted(read_jobs().values(), key=lambda job: job.get("created_at", ""), reverse=True)


@app.post("/api/jobs")
async def create_job(background_tasks: BackgroundTasks, video: UploadFile = File(...), clip_limit: int = 20) -> dict[str, Any]:
    if clip_limit < 1 or clip_limit > 50:
        raise HTTPException(status_code=400, detail="clip_limit must be between 1 and 50.")
    original_name = safe_name(video.filename or "video.mp4")
    if Path(original_name).suffix.lower() not in ALLOWED_SUFFIXES:
        raise HTTPException(status_code=400, detail="Upload an MP4, MOV, MKV, WEBM, or M4V video.")
    job_id = new_id()
    filename = f"{job_id}_{original_name}"
    destination = UPLOAD_DIR / filename
    size = 0
    try:
        with destination.open("wb") as output:
            while chunk := await video.read(1024 * 1024):
                size += len(chunk)
                if size > MAX_UPLOAD_BYTES:
                    raise HTTPException(status_code=413, detail="Video exceeds the 2 GB local MVP limit.")
                output.write(chunk)
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    finally:
        await video.close()
    if size == 0:
        destination.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")
    from datetime import datetime, timezone
    job = {"id": job_id, "name": Path(original_name).stem, "filename": filename, "status": "queued", "created_at": datetime.now(timezone.utc).isoformat(), "clip_limit": clip_limit, "source_name": original_name, "clips": [], "error": None}
    jobs = read_jobs()
    jobs[job_id] = job
    write_jobs(jobs)
    background_tasks.add_task(_analyze, job_id)
    return job


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str) -> dict[str, Any]:
    return _get_job(job_id)


@app.post("/api/jobs/{job_id}/analyze")
def analyze_again(job_id: str, background_tasks: BackgroundTasks) -> dict[str, str]:
    job = _get_job(job_id)
    if job.get("status") in {"queued", "analyzing"}:
        raise HTTPException(status_code=409, detail="This project is already being analyzed.")
    job.update({"status": "queued", "error": None})
    jobs = read_jobs()
    jobs[job_id] = job
    write_jobs(jobs)
    background_tasks.add_task(_analyze, job_id)
    return {"status": "queued"}


@app.post("/api/jobs/{job_id}/render")
def create_render(job_id: str, request: RenderRequest) -> dict[str, str]:
    job = _get_job(job_id)
    clips = job.get("clips", [])
    if request.clip_index >= len(clips):
        raise HTTPException(status_code=404, detail="Clip suggestion not found.")
    try:
        output = render_clip(job_id, request.clip_index + 1, UPLOAD_DIR / job["filename"], clips[request.clip_index]["start"], clips[request.clip_index]["end"], request.layout)
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Render failed: {exc}") from exc
    return {"download_url": f"/api/exports/{output.name}", "filename": output.name}


@app.get("/api/exports/{filename}")
def download_export(filename: str) -> FileResponse:
    path = (EXPORT_DIR / Path(filename).name).resolve()
    if path.parent != EXPORT_DIR.resolve() or not path.is_file():
        raise HTTPException(status_code=404, detail="Export not found.")
    return FileResponse(path, media_type="video/mp4", filename=path.name)


@app.delete("/api/jobs/{job_id}")
def delete_job(job_id: str) -> dict[str, str]:
    job = _get_job(job_id)
    (UPLOAD_DIR / job["filename"]).unlink(missing_ok=True)
    for path in EXPORT_DIR.glob(f"{job_id}-*.mp4"):
        path.unlink(missing_ok=True)
    jobs = read_jobs()
    jobs.pop(job_id, None)
    write_jobs(jobs)
    return {"status": "deleted"}
