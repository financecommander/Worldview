from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class WorldState:
    timestamp: float
    entities: Dict[str, Dict[str, Any]]
    environment: Dict[str, Any]

    def update_entity(self, entity_id: str, properties: Dict[str, Any]):
        """Update properties of an entity in the world state."""
        self.entities[entity_id].update(properties)

@dataclass
class TemporalSceneGraph:
    states: List[WorldState]

    def add_state(self, state: WorldState):
        """Add a new world state to the temporal graph."""
        self.states.append(state)

    def get_state_at(self, timestamp: float) -> WorldState:
        """Retrieve the world state closest to the given timestamp."""
        if not self.states:
            raise ValueError("No states available in the scene graph.")
        return min(self.states, key=lambda s: abs(s.timestamp - timestamp))

    def interpolate_state(self, timestamp: float) -> WorldState:
        """Interpolate between states for a given timestamp (basic linear for now)."""
        # TODO: Implement proper interpolation logic for entity properties and environment
        return self.get_state_at(timestamp)
