import sqlite3
from typing import List, Any
from dataclasses import dataclass
import json

@dataclass
class SearchResult:
    event_id: int
    frame_idx: int
    timestamp: float
    score: float

class SemanticEventStore:
    def __init__(self, db_path: str = "worldview.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                frame_idx INTEGER,
                timestamp REAL,
                objects TEXT,
                embeddings BLOB,
                text TEXT
            )
        """)
        self.conn.commit()

    def store_events(self, events: List[Any]):
        for event in events:
            self.conn.execute("""
                INSERT INTO events (frame_idx, timestamp, objects, embeddings, text)
                VALUES (?, ?, ?, ?, ?)
            """, (
                event.frame_idx,
                event.timestamp,
                json.dumps(event.objects),
                event.embeddings.tobytes(),
                event.text
            ))
        self.conn.commit()

    def search_events(self, query: str, limit: int = 10) -> List[SearchResult]:
        # TODO: Implement semantic search with embeddings
        cursor = self.conn.execute("SELECT id, frame_idx, timestamp FROM events LIMIT ?", (limit,))
        return [SearchResult(row[0], row[1], row[2], 1.0) for row in cursor.fetchall()]