import sqlite3
import json

conn = sqlite3.connect("diary.db", check_same_thread=False)
cursor = conn.cursor()

# 테이블 생성
cursor.execute("""
CREATE TABLE IF NOT EXISTS diary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    summary TEXT,
    emotions TEXT,
    embedding TEXT
)
""")

conn.commit()


def save_diary(text, summary, emotions, embedding):
    cursor.execute(
        "INSERT INTO diary (text, summary, emotions, embedding) VALUES (?, ?, ?, ?)",
        (text, summary, json.dumps(emotions), json.dumps(embedding))
    )
    conn.commit()


def get_all_diaries():
    cursor.execute("SELECT * FROM diary")
    return cursor.fetchall()