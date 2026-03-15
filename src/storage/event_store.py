import sqlite3
from dataclasses import dataclass
from typing import List, Any
import json

@dataclass
class SearchResult:
    event_id: int
    frame_id: int
    timestamp: float
    metadata: dict

class SemanticEventStore:
    def __init__(self, db_path: str = "events.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    frame_id INTEGER,
                    timestamp REAL,
                    detections TEXT,
                    embeddings BLOB,
                    ocr_text TEXT
                )
            """)
            conn.commit()

    def store_events(self, events: List[Any]):
        with sqlite3.connect(self.db_path) as conn:
            for event in events:
                conn.execute("""
                    INSERT INTO events (frame_id, timestamp, detections, embeddings, ocr_text)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    event.frame_id,
                    event.timestamp,
                    json.dumps(event.detections),
                    event.embeddings.tobytes(),
                    event.ocr_text
                ))
            conn.commit()

    def search_events(self, query: str) -> List[SearchResult]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id, frame_id, timestamp, detections FROM events WHERE ocr_text LIKE ?", (f"%{query}%",))
            return [SearchResult(id=row[0], frame_id=row[1], timestamp=row[2], metadata=json.loads(row[3])) for row in cursor.fetchall()]
