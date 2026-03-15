from fastapi import FastAPI, HTTPException
from typing import List
import numpy as np
from perception.detection import detect_objects
from compression.embeddings import generate_embeddings
from storage.search import SemanticSearch
from generation.video import generate_video

app = FastAPI(title="Worldview API")
search_db = SemanticSearch()

@app.on_event("shutdown")
async def shutdown_db():
    search_db.close()

@app.post("/process-video")
async def process_video(video_frames: List[Any]):
    try:
        # Mock video frames as numpy arrays for now
        frames = [np.zeros((480, 640, 3)) for _ in range(len(video_frames))]
        detections = await detect_objects(frames)
        embeddings = await generate_embeddings(detections)
        video_id = "test_video"
        for frame_id, emb in enumerate(embeddings):
            search_db.store_embedding(video_id, frame_id, emb)
        generated_path = await generate_video(detections, embeddings)
        return {"status": "success", "video_path": generated_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def search_similar(query: Any):
    # Mock query embedding
    query_emb = np.random.rand(128)
    results = search_db.search_similar(query_emb)
    return {"results": results}
