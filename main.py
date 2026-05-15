from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from maru import generate_maru

from prompt import make_prompt
from utils import safe_parse
from db import save_diary, get_all_diaries
from embedding import get_embedding, find_similar

app = FastAPI()

import os
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

class DiaryRequest(BaseModel):
    text: str


@app.post("/analyze")
def analyze(req: DiaryRequest):

    # 1. 감정 분석
    prompt = make_prompt(req.text)

    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0.2}
    )

    raw_output = response.text
    parsed = safe_parse(raw_output)

    # 2. 임베딩 생성
    embedding = get_embedding(req.text)

    # 3. 과거 데이터 불러오기
    diaries = get_all_diaries()

    # 4. 유사 일기 찾기
    similar, score = find_similar(embedding, diaries) if diaries else (None, None)

    # 5. DB 저장
    save_diary(
        req.text,
        parsed["summary"],
        parsed["emotions"],
        embedding
    )
    
    # 6. 마루 메모 생성
    maru_memo = generate_maru(parsed, similar, score)
    
    return {
        "analysis": parsed,
        "similar_diary": similar,
        "similarity_score": score,
        "maru_memo": maru_memo
    }