def make_prompt(diary_text):

    return f"""
너는 감정 분석기다.

반드시 JSON만 출력해.
절대 설명, 문장, 마크다운, ``` 포함 금지.

JSON 외 아무것도 출력하면 안 된다.

형식:
{{
    "summary": "...",
    "emotions": ["..."],
    "events": ["..."],
    "persons": ["..."],
    "emotion_intensity": "low|medium|high",
    "emotion_polarity": "positive|negative|mixed"
}}

일기:
{diary_text}
"""