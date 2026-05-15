import numpy as np
import google.generativeai as genai
import json

# Gemini embedding 모델
embed_model = genai.GenerativeModel("embedding-001")


def get_embedding(text):
    response = genai.embed_content(
        model="models/embedding-001",
        content=text
    )
    return response["embedding"]


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def find_similar(new_embedding, diaries):

    best = None
    best_score = -1

    for diary in diaries:
        old_embedding = json.loads(diary[4])  # embedding column

        score = cosine_similarity(new_embedding, old_embedding)

        if score > best_score:
            best_score = score
            best = diary

    return best, best_score