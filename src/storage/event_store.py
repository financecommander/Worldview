import sqlite3
from typing import List, Any
from dataclasses import dataclass
import json

@dataclass
class EventQuery:
    text: str = ''
    object_type: str = ''
    time_range: tuple = (0.0, float('inf'))

class EventStore:
    def __init__(self, db_path: str = 'events.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    frame_id INTEGER,
                    timestamp REAL,
                    objects TEXT,
                    embeddings BLOB,
                    ocr_text TEXT
                )
            ''')

    def store_event(self, event: Any):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO events (frame_id, timestamp, objects, embeddings, ocr_text)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                event.frame_id,
                event.timestamp,
                json.dumps(event.objects),
                event.embeddings.tobytes(),
                event.ocr_text
            ))
            conn.commit()

    def search(self, query: EventQuery) -> List[Any]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            sql = '''
                SELECT * FROM events 
                WHERE timestamp BETWEEN ? AND ?
            '''
            params = [query.time_range[0], query.time_range[1]]
            if query.text:
                sql += " AND ocr_text LIKE ?"
                params.append(f"%{query.text}%")
            cursor.execute(sql, params)
            return cursor.fetchall()
