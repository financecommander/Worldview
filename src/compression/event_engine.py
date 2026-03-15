from dataclasses import dataclass
from typing import List, Dict, Any
import numpy as np

@dataclass
class SemanticEvent:
    frame_idx: int
    timestamp: float
    detections: List[Dict[str, Any]]
    embeddings: np.ndarray
    ocr_text: str
    tracking_ids: List[int]

class EventCompressionEngine:
    def __init__(self, model_client):
        self.model_client = model_client

    async def compress_frame(self, frame_idx: int, frame: np.ndarray, timestamp: float) -> SemanticEvent:
        """
        Compress a single frame into a semantic event with detections, embeddings, OCR, and tracking.
        """
        # TODO: Wire up actual model inference via Triton client
        detections = await self.model_client.detect_objects(frame)
        embeddings = await self.model_client.get_embeddings(frame)
        ocr_text = await self.model_client.extract_text(frame)
        tracking_ids = await self.model_client.track_objects(frame)

        return SemanticEvent(
            frame_idx=frame_idx,
            timestamp=timestamp,
            detections=detections or [],
            embeddings=embeddings if embeddings is not None else np.array([]),
            ocr_text=ocr_text or "",
            tracking_ids=tracking_ids or []
        )

    async def process_video(self, video_path: str, sampler) -> List[SemanticEvent]:
        """Process a full video into a list of semantic events."""
        keyframes = sampler.extract_keyframes(video_path)
        events = []
        for frame_idx, frame in keyframes:
            timestamp = frame_idx / 30.0  # Assuming 30 FPS
            event = await self.compress_frame(frame_idx, frame, timestamp)
            events.append(event)
        return events
