"""Database Manager - SQLite chat history storage"""
import aiosqlite
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import os


class DatabaseManager:
    """Manages SQLite database for chat history"""
    
    def __init__(self, db_path="backend/db/chat_history.db"):
        self.db_path = db_path
        self.conn: Optional[aiosqlite.Connection] = None
    
    async def initialize(self):
        """Initialize database and create tables"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        self.conn = await aiosqlite.connect(self.db_path)
        
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                metadata TEXT
            )
        """)
        
        await self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_session_timestamp 
            ON chat_history(session_id, timestamp)
        """)
        
        await self.conn.commit()
        print("✅ Database initialized")
    
    async def save_message(
        self,
        session_id: str,
        role: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Save chat message to database"""
        timestamp = datetime.utcnow().isoformat()
        metadata_json = json.dumps(metadata) if metadata else None
        
        await self.conn.execute(
            """
            INSERT INTO chat_history (session_id, timestamp, role, message, metadata)
            VALUES (?, ?, ?, ?, ?)
            """,
            (session_id, timestamp, role, message, metadata_json)
        )
        await self.conn.commit()
    
    async def get_messages(self, session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve chat history for a session"""
        cursor = await self.conn.execute(
            """
            SELECT timestamp, role, message, metadata
            FROM chat_history
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (session_id, limit)
        )
        
        rows = await cursor.fetchall()
        messages = []
        
        for row in rows:
            messages.append({
                "timestamp": row[0],
                "role": row[1],
                "message": row[2],
                "metadata": json.loads(row[3]) if row[3] else None
            })
        
        return list(reversed(messages))  # Return in chronological order
    
    async def close(self):
        """Close database connection"""
        if self.conn:
            await self.conn.close()
