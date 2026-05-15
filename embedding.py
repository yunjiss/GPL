import numpy as np
import google.generativeai as genai
import json

def get_embedding(text):
    response = genai.embed_content(
        model="models/embedding-001",
        content=text
    )
    return response["embedding"]

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    # 0 분모 에러 방지
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return np.dot(a, b) / (norm_a * norm_b)

def find_similar(new_embedding, diaries):
    best = None
    best_score = -1

    for diary in diaries:
        # db.py에서 딕셔너리로 넘겨주므로 키 값("embedding")으로 접근
        old_embedding = json.loads(diary["embedding"]) 
        score = cosine_similarity(new_embedding, old_embedding)

        if score > best_score:
            best_score = score
            best = diary

    return best, best_score