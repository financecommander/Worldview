import cv2
import numpy as np
from typing import List, Tuple

class FrameSampler:
    def __init__(self, sample_interval: int = 30):
        self.sample_interval = sample_interval

    def extract_keyframes(self, video_path: str) -> List[Tuple[int, np.ndarray]]:
        """
        Extract keyframes from a video at the specified interval.
        Returns list of (frame_index, frame_data) tuples.
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        keyframes = []
        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_idx % self.sample_interval == 0:
                keyframes.append((frame_idx, frame))
            frame_idx += 1

        cap.release()
        return keyframes

    def save_frames(self, frames: List[Tuple[int, np.ndarray]], output_dir: str):
        """Save extracted frames to disk."""
        import os
        os.makedirs(output_dir, exist_ok=True)
        for idx, (_, frame) in enumerate(frames):
            cv2.imwrite(f"{output_dir}/frame_{idx}.jpg", frame)
