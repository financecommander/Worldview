import cv2
import numpy as np
from typing import List, Optional

class FrameSampler:
    def __init__(self, interval: int = 30):
        self.interval = interval

    def sample(self, video_path: str) -> List[np.ndarray]:
        """Extract frames from video at specified interval."""
        cap = cv2.VideoCapture(video_path)
        frames = []
        frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % self.interval == 0:
                frames.append(frame)
            frame_count += 1
        
        cap.release()
        return frames

    def get_keyframes(self, video_path: str, max_frames: Optional[int] = None) -> List[np.ndarray]:
        """Get keyframes up to a maximum number."""
        frames = self.sample(video_path)
        if max_frames and len(frames) > max_frames:
            return frames[:max_frames]
        return frames
