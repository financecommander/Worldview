from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
import os
import cv2
from perception.frame_sampler import FrameSampler
from compression.event_engine import EventCompressionEngine
from storage.event_store import SemanticEventStore

app = FastAPI(title="Worldview Video Intelligence Platform")

# TODO: Inject actual Triton client dependency
model_client = None
event_engine = EventCompressionEngine(model_client)
event_store = SemanticEventStore()
sampler = FrameSampler(interval_seconds=1.0)

@app.post("/ingest")
async def ingest_video(file: UploadFile = File(...)):
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    try:
        frames = sampler.extract_keyframes(temp_path)
        cap = cv2.VideoCapture(temp_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        events = await event_engine.process_video_frames(frames, fps)
        for event in events:
            event_store.store_event(event)
        return {"status": "success", "events_processed": len(events)}
    finally:
        os.remove(temp_path)

@app.get("/search")
async def search_events(query: str, limit: int = 10):
    results = event_store.search_events(query, limit)
    return {"results": [r.__dict__ for r in results]}
