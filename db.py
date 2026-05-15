import sqlite3
import json

conn = sqlite3.connect("diary.db", check_same_thread=False)
# 컬럼 이름으로 데이터에 접근하기 위해 row_factory 설정
conn.row_factory = sqlite3.Row 
cursor = conn.cursor()

# 테이블 구조 확장
cursor.execute("""
CREATE TABLE IF NOT EXISTS diary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    summary TEXT,
    emotions TEXT,
    events TEXT,
    persons TEXT,
    emotion_intensity TEXT,
    emotion_polarity TEXT,
    followup_question TEXT,
    embedding TEXT
)
""")
conn.commit()

def save_diary(text, parsed_data, embedding):
    cursor.execute(
        """INSERT INTO diary 
        (text, summary, emotions, events, persons, emotion_intensity, emotion_polarity, followup_question, embedding) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            text, 
            parsed_data.get("summary", ""), 
            json.dumps(parsed_data.get("emotions", [])),
            json.dumps(parsed_data.get("events", [])),
            json.dumps(parsed_data.get("persons", [])),
            parsed_data.get("emotion_intensity", "medium"),
            parsed_data.get("emotion_polarity", "mixed"),
            parsed_data.get("followup_question", ""),
            json.dumps(embedding)
        )
    )
    conn.commit()

def get_all_diaries():
    cursor.execute("SELECT * FROM diary")
    # Row 객체를 딕셔너리로 변환하여 반환
    return [dict(row) for row in cursor.fetchall()]