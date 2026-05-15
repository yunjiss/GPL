import google.generativeai as genai
import os
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_maru(current, similar, score):

    # 과거 데이터 없을 때
    if similar is None:
        return "오늘 느낀 감정을 천천히 정리해보는 것도 괜찮을 것 같아."

    prompt = f"""
너는 사용자의 과거 기록을 기반으로
현재를 도와주는 조용한 조언자야.

절대:
- 훈계하지 마
- 일반적인 위로 금지
- 뻔한 말 금지

반드시:
- 과거 경험을 근거로 말하기
- 선택지 2개 제시하기
- 3문장 이내

현재 상황:
{current["summary"]}

현재 감정:
{current["emotions"]}

과거 유사 경험:
{similar[2]}  # summary

유사도:
{score}

출력 형식:
- 한 줄 공감
- 선택지 2개
"""

    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0.4}
    )

    return response.text