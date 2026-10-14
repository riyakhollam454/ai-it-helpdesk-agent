import sqlite3
from datetime import datetime
from pathlib import Path


DB_PATH = Path(__file__).parent / "helpdesk.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    # Conversation memory
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Long-term memory
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            memory TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Tickets
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT,
            priority TEXT,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Email log
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            recipient TEXT NOT NULL,
            subject TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ------------------------------------------------
# CONVERSATION MEMORY
# ------------------------------------------------

def save_message(user_id, role, message):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO conversations
        (user_id, role, message, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            role,
            message,
            datetime.utcnow().isoformat()
        )
    )

    conn.commit()
    conn.close()


def get_recent_messages(user_id, limit=10):

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT role, message, created_at
        FROM conversations
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (user_id, limit)
    ).fetchall()

    conn.close()

    return list(reversed([dict(row) for row in rows]))


# ------------------------------------------------
# LONG-TERM MEMORY
# ------------------------------------------------

def save_memory(user_id, memory):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO memories
        (user_id, memory, created_at)
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            memory,
            datetime.utcnow().isoformat()
        )
    )

    conn.commit()
    conn.close()


def get_memories(user_id, limit=10):

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT memory, created_at
        FROM memories
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (user_id, limit)
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]