from typing import List
import numpy as np

async def generate_embeddings(detections: List[dict]) -> List[np.ndarray]:
    """
    Generate embeddings for detected objects in video frames.
    Returns list of embeddings per frame.
    """
    # TODO: Integrate real embedding model via Triton or local inference
    return mock_embeddings(len(detections))

def mock_embeddings(num_frames: int) -> List[np.ndarray]:
    """Generate mock embeddings for local development."""
    return [np.random.rand(128) for _ in range(num_frames)]
