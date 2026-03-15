from dataclasses import dataclass
from typing import List, Dict, Any
import numpy as np

@dataclass
class SemanticEvent:
    frame_id: int
    timestamp: float
    detections: List[Dict[str, Any]]
    embeddings: np.ndarray
    ocr_text: str

class EventCompressionEngine:
    def __init__(self, model_client: Any):
        self.model_client = model_client

    async def compress_frame(self, frame_id: int, frame: np.ndarray, timestamp: float) -> SemanticEvent:
        """
        Compress a single frame into a semantic event with detections, embeddings, and OCR.
        """
        # TODO: Wire up actual model inference via Triton client
        detections = await self.model_client.detect_objects(frame)
        embeddings = await self.model_client.get_embeddings(frame)
        ocr_text = await self.model_client.extract_text(frame)
        return SemanticEvent(
            frame_id=frame_id,
            timestamp=timestamp,
            detections=detections or [],
            embeddings=embeddings if embeddings is not None else np.array([]),
            ocr_text=ocr_text or ""
        )

    async def process_video_frames(self, frames: List[Tuple[int, np.ndarray]], fps: float) -> List[SemanticEvent]:
        """Process a list of frames into semantic events."""
        events = []
        for frame_id, frame in frames:
            timestamp = frame_id / fps
            event = await self.compress_frame(frame_id, frame, timestamp)
            events.append(event)
        return events
