import sqlite3
from dataclasses import dataclass
from typing import List, Any
import json

@dataclass
class EventQueryResult:
    event_id: int
    frame_idx: int
    timestamp: float
    data: dict

class SemanticEventStore:
    def __init__(self, db_path: str = "events.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite database with events table."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                frame_idx INTEGER,
                timestamp REAL,
                data TEXT
            )
        """)
        conn.commit()
        conn.close()

    def store_event(self, event: Any):
        """Store a semantic event in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        data_json = json.dumps({
            "detections": event.detections,
            "ocr_text": event.ocr_text,
            "tracking_ids": event.tracking_ids
        })
        cursor.execute(
            "INSERT INTO events (frame_idx, timestamp, data) VALUES (?, ?, ?)",
            (event.frame_idx, event.timestamp, data_json)
        )
        conn.commit()
        conn.close()

    def search_events(self, query: str, limit: int = 10) -> List[EventQueryResult]:
        """Search events based on a simple text query."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, frame_idx, timestamp, data FROM events WHERE data LIKE ? LIMIT ?",
            (f"%{query}%", limit)
        )
        rows = cursor.fetchall()
        conn.close()
        return [EventQueryResult(id=row[0], frame_idx=row[1], timestamp=row[2], data=json.loads(row[3])) for row in rows]
