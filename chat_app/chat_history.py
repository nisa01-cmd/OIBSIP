# chat_history.py
import sqlite3
from datetime import datetime

def init_chat_db():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        message TEXT,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

def save_message(username, message):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO messages (username, message, timestamp) VALUES (?, ?, ?)",
              (username, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def load_messages(username):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("SELECT message, timestamp FROM messages WHERE username=? ORDER BY id", (username,))
    rows = c.fetchall()
    conn.close()
    return rows
