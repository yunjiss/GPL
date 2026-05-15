import google.generativeai as genai
import os

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_maru(current, similar, score):
    # 유사한 과거 데이터가 없거나 유사도가 낮을 때
    if similar is None or score < 0.7:
        emotions_str = ", ".join(current.get('emotions', []))
        return f"오늘은 {emotions_str} 감정이 느껴졌구나. 푹 쉬면서 마음을 다독이는 시간을 가져보면 어떨까?"

    prompt = f"""
너는 사용자의 과거를 기억하고 오늘을 다독이는 조언자 '마루'야.
아래 정보를 바탕으로 과거의 경험과 연결된 따뜻한 메시지를 작성해줘.

- 현재 요약: {current.get('summary')}
- 현재 감정: {current.get('emotions')}
- 과거 유사 경험: {similar.get('summary')}

[규칙]
1. 한 줄로 공감하기.
2. 과거의 경험을 언급하며 "예전에도 비슷한 일이 있었는데, 그때와 비교하면 지금은 어때?"라는 뉘앙스로 묻기.
3. 현재 도움이 될만한 가벼운 행동 선택지 2개 제안하기.
4. 전체 3~4문장 이내.

메시지:"""

    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0.4}
    )

    return response.text