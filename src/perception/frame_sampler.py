import cv2
import numpy as np
from typing import List, Tuple

class FrameSampler:
    def __init__(self, sample_interval: int = 30):
        self.sample_interval = sample_interval

    def sample_frames(self, video_path: str) -> List[Tuple[int, np.ndarray]]:
        """
        Extract keyframes from a video at specified intervals.
        Returns list of (frame_index, frame_array) tuples.
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")

        frames = []
        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_idx % self.sample_interval == 0:
                frames.append((frame_idx, frame))
            frame_idx += 1

        cap.release()
        return frames