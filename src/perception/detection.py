from typing import List, Dict, Any
import numpy as np

async def detect_objects(video_frames: List[np.ndarray]) -> List[Dict[str, Any]]:
    """
    Detect objects in video frames using Triton inference server or mock data.
    Returns list of detections per frame with bounding boxes and labels.
    """
    try:
        # TODO: Integrate Triton client for real inference
        return mock_detections(len(video_frames))
    except Exception as e:
        print(f"Triton detection failed: {e}, falling back to mock data")
        return mock_detections(len(video_frames))

def mock_detections(num_frames: int) -> List[Dict[str, Any]]:
    """Generate mock detection data for local development."""
    detections = []
    for _ in range(num_frames):
        frame_dets = {
            "boxes": [[100, 100, 200, 200], [300, 300, 400, 400]],
            "labels": ["person", "car"],
            "scores": [0.9, 0.85]
        }
        detections.append(frame_dets)
    return detections
