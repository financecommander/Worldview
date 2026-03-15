from typing import List, Dict, Any

from .scene_graph import TemporalSceneGraph

class KeyframeGenerator:
    def __init__(self, scene_graph: TemporalSceneGraph):
        self.scene_graph = scene_graph

    def generate_keyframes(self, timestamps: List[float]) -> List[Dict[str, Any]]:
        """Generate keyframes for the given timestamps."""
        keyframes = []
        for ts in timestamps:
            state = self.scene_graph.get_state_at(ts)
            keyframes.append({
                "timestamp": ts,
                "entities": state.entities,
                "environment": state.environment
            })
        return keyframes
