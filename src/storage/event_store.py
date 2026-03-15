import sqlite3
from typing import List, Any
from dataclasses import dataclass
import json

@dataclass
class EventQueryResult:
    event_id: int
    frame_id: int
    timestamp: float
    detections: List[Any]
    ocr_text: str

class SemanticEventStore:
    def __init__(self, db_path: str = "events.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    frame_id INTEGER,
                    timestamp REAL,
                    detections TEXT,
                    embeddings BLOB,
                    ocr_text TEXT
                )
            """)
            conn.commit()

    def store_event(self, event: Any):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO events (frame_id, timestamp, detections, embeddings, ocr_text)
                VALUES (?, ?, ?, ?, ?)
            """, (
                event.frame_id,
                event.timestamp,
                json.dumps(event.detections),
                event.embeddings.tobytes() if event.embeddings.size > 0 else b'',
                event.ocr_text
            ))
            conn.commit()

    def search_events(self, query: str, limit: int = 10) -> List[EventQueryResult]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT event_id, frame_id, timestamp, detections, ocr_text
                FROM events
                WHERE ocr_text LIKE ? OR detections LIKE ?
                LIMIT ?
            """, (f"%{query}%", f"%{query}%", limit))
            return [EventQueryResult(
                event_id=row[0],
                frame_id=row[1],
                timestamp=row[2],
                detections=json.loads(row[3]),
                ocr_text=row[4]
            ) for row in cursor.fetchall()]
