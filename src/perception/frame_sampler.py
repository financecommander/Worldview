import cv2
import numpy as np
from typing import List, Tuple

class FrameSampler:
    def __init__(self, interval_seconds: float = 1.0):
        self.interval_seconds = interval_seconds

    def extract_keyframes(self, video_path: str) -> List[Tuple[int, np.ndarray]]:
        """
        Extract keyframes from a video at specified intervals.
        Returns list of (frame_id, frame_data) tuples.
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * self.interval_seconds)
        keyframes = []
        frame_id = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_id % frame_interval == 0:
                keyframes.append((frame_id, frame))
            frame_id += 1

        cap.release()
        return keyframes

    def save_frame(self, frame: np.ndarray, output_path: str):
        """Save a frame to disk."""
        cv2.imwrite(output_path, frame)
