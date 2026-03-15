from fastapi import FastAPI, HTTPException, UploadFile, File
from typing import List
import os

from ..perception.frame_sampler import FrameSampler
from ..compression.event_engine import EventCompressionEngine
from ..storage.event_store import SemanticEventStore

app = FastAPI(title="Worldview Video Intelligence API")

# TODO: Inject actual model client
model_client = None
sampler = FrameSampler(sample_interval=30)
engine = EventCompressionEngine(model_client)
store = SemanticEventStore()

@app.post("/ingest")
async def ingest_video(file: UploadFile = File(...)):
    """Ingest a video file and process it into semantic events."""
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    try:
        events = await engine.process_video(temp_path, sampler)
        for event in events:
            store.store_event(event)
        return {"status": "success", "event_count": len(events)}
    finally:
        os.remove(temp_path)

@app.get("/search")
async def search_events(query: str, limit: int = 10):
    """Search for semantic events based on a query."""
    results = store.search_events(query, limit)
    return {"results": [r.__dict__ for r in results]}

@app.post("/generate")
async def generate_clip(event_ids: List[int]):
    """Generate a video clip from a list of event IDs."""
    # TODO: Implement reconstruction logic
    return {"status": "not_implemented"}

@app.get("/events")
async def list_events(limit: int = 100):
    """List recent events."""
    return {"events": store.search_events("", limit)}
