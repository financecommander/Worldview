from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
import os
from src.perception.frame_sampler import FrameSampler
from src.compression.event_engine import EventCompressionEngine
from src.storage.event_store import SemanticEventStore

app = FastAPI(title="Worldview Video Intelligence")

sampler = FrameSampler()
engine = EventCompressionEngine()
store = SemanticEventStore()

@app.post("/ingest")
async def ingest_video(file: UploadFile = File(...)):
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    try:
        frames = sampler.sample_frames(temp_path)
        events = engine.compress_frames(frames)
        store.store_events(events)
        return {"status": "success", "events": len(events)}
    finally:
        os.remove(temp_path)

@app.get("/search")
async def search_events(query: str, limit: int = 10):
    results = store.search_events(query, limit)
    return {"results": [r.__dict__ for r in results]}

@app.post("/generate")
async def generate_clip(event_ids: List[int]):
    # TODO: Implement clip generation logic
    return {"status": "clip generation not implemented"}

@app.get("/events")
async def list_events(limit: int = 100):
    results = store.search_events("", limit)
    return {"events": [r.__dict__ for r in results]}