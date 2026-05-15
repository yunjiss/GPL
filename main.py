from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv() 

import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

from maru import generate_maru
from prompt import make_prompt
from utils import safe_parse
from db import save_diary, get_all_diaries
from embedding import get_embedding, find_similar

app = FastAPI()
model = genai.GenerativeModel("gemini-1.5-flash")

class DiaryRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze(req: DiaryRequest):
    # 1. 감정 분석 및 구조화
    prompt = make_prompt(req.text)
    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0.2}
    )
    parsed = safe_parse(response.text)

    # 2. 임베딩 생성
    embedding = get_embedding(req.text)

    # 3. 과거 데이터 불러오기
    diaries = get_all_diaries()

    # 4. 유사 일기 찾기
    similar, score = find_similar(embedding, diaries) if diaries else (None, 0.0)

    # 5. DB 저장
    save_diary(req.text, parsed, embedding)
    
    # 6. 마루 메모 생성 (현재 일기와 유사했던 과거를 비교)
    maru_memo = generate_maru(parsed, similar, score)
    
    return {
        "analysis": parsed,
        "maru_memo": maru_memo,
        "past_connection": {
            "is_connected": score > 0.7 if score else False,
            "past_summary": similar.get("summary") if similar else None,
            "similarity_score": float(score) if score else 0.0
        }
    }