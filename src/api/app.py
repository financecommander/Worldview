from fastapi import FastAPI, UploadFile, File, Query
from typing import List
import os

from perception.frame_sampler import FrameSampler
from compression.event_engine import EventCompressionEngine
from storage.event_store import SemanticEventStore, SearchResult

app = FastAPI(title="Worldview Video Intelligence API")

event_store = SemanticEventStore()

@app.post("/ingest")
async def ingest_video(file: UploadFile = File(...)):
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    sampler = FrameSampler(interval_seconds=1.0)
    frames = sampler.sample_frames(temp_path)
    engine = EventCompressionEngine()
    events = engine.compress_frames(frames)
    event_store.store_events(events)
    os.remove(temp_path)
    return {"status": "ingested", "event_count": len(events)}

@app.get("/search", response_model=List[SearchResult])
async def search_events(query: str = Query(...)):
    return event_store.search_events(query)

@app.post("/generate")
async def generate_clip(event_ids: List[int]):
    # TODO: Implement clip generation from event IDs
    return {"status": "generated", "clip_url": "/clips/generated.mp4"}

@app.get("/events")
async def list_events():
    return event_store.search_events("")
