import sqlite3
import os
import shutil
from datetime import datetime

# Use /tmp for writable operations
TMP_DB_PATH = "/tmp/db/chatbot.db"
PROJECT_DB_PATH = "db/chatbot.db"

# Copy existing database from project to /tmp if it doesn't exist in /tmp
os.makedirs('/tmp/db', exist_ok=True)

if not os.path.exists(TMP_DB_PATH) and os.path.exists(PROJECT_DB_PATH):
    shutil.copy2(PROJECT_DB_PATH, TMP_DB_PATH)
    print(f"✅ Copied database from {PROJECT_DB_PATH} to {TMP_DB_PATH}")

DB_PATH = TMP_DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            thread_name TEXT,
            role TEXT,
            message TEXT,
            created_at TEXT
        )
        """
    )

    conn.commit()
    conn.close()
    print(f"✅ Database initialized at {DB_PATH}")



def save_message(thread_name, role, message):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chats(thread_name, role, message, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            thread_name,
            role,
            message,
            datetime.utcnow().isoformat()
        )
    )

    conn.commit()
    conn.close()


def get_threads():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT DISTINCT thread_name
        FROM chats
        ORDER BY thread_name DESC
        """
    )

    data = cursor.fetchall()

    conn.close()

    return [row[0] for row in data]


def get_thread_messages(thread_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, message
        FROM chats
        WHERE thread_name = ?
        ORDER BY created_at ASC
        """,
        (thread_name,)
    )

    data = cursor.fetchall()

    conn.close()

    return data


def delete_thread(thread_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM chats
        WHERE thread_name = ?
        """,
        (thread_name,)
    )

    conn.commit()
    conn.close()