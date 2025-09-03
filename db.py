import sqlite3
from datetime import datetime, date
from pathlib import Path

DB_PATH = Path("data/chat_log.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            role TEXT,
            system_prompt TEXT,
            question TEXT,
            answer TEXT,
            image_path TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()

def get_connection():
    return sqlite3.connect(DB_PATH)

def insert_chat_log(user_id, role, system_prompt, question, answer, image_path=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
            INSERT INTO chat_logs (user_id, role, system_prompt, question, answer, image_path)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, role, system_prompt, question, answer, image_path))
    conn.commit()
    conn.close()

def get_user_chat_logs(user_id, limit=5, offset=0):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
        SELECT timestamp, role, question, answer FROM chat_logs
        WHERE user_id = ? ORDER BY timestamp DESC LIMIT ? OFFSET ?
        ''', (user_id, limit, offset))
        return c.fetchall()

def count_user_queries(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM chat_logs WHERE user_id = ?", (user_id,))
        return c.fetchone()[0]

def count_user_queries_today(user_id):
    today = date.today().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM chat_logs WHERE user_id = ? AND DATE(timestamp) = ?", (user_id, today))
        return c.fetchone()[0]
