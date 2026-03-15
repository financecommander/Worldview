from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List, Any
import os

from perception.frame_sampler import FrameSampler
from compression.event_engine import EventCompressionEngine
from storage.event_store import EventStore, EventQuery

app = FastAPI(title="Worldview Video Intelligence Platform")

# Dependencies (TODO: Use proper DI)
sampler = FrameSampler(interval=30)
store = EventStore()
engine = EventCompressionEngine(model_client=None)  # TODO: Wire up Triton client

@app.post("/ingest")
async def ingest_video(file: UploadFile = File(...)):
    """Ingest a video file and process it into semantic events."""
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    try:
        frames = sampler.sample(temp_path)
        events = await engine.process_video(frames, fps=30.0)
        for event in events:
            store.store_event(event)
        return {"status": "success", "events": len(events)}
    finally:
        os.remove(temp_path)

@app.get("/search")
async def search_events(text: str = '', start_time: float = 0.0, end_time: float = float('inf')):
    """Search for events based on text and time range."""
    query = EventQuery(text=text, time_range=(start_time, end_time))
    results = store.search(query)
    return {"results": results}

@app.post("/generate")
async def generate_clip(data: dict):
    """Generate a video clip from semantic events (placeholder)."""
    # TODO: Implement reconstruction logic
    return {"status": "clip generation not implemented"}

@app.get("/events")
async def list_events():
    """List all stored events."""
    with sqlite3.connect(store.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events")
        return {"events": cursor.fetchall()}
