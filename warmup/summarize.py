from google import genai
from dotenv import load_dotenv
from google.genai import errors
from google.genai import types
import os
import sys
import time

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

filename = sys.argv[1]
with open(file=filename, mode="r", encoding="UTF-8") as f:
    text = f.read()

config = types.GenerateContentConfig(
    system_instruction="너는 요약 전문가. 한국어 텍스트를 정확히 5줄로 요약. 다른 말 X."
)

def safe_generate(client, model, contents, config=None, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model = model,
                contents = contents,
                config = config
            )
        except errors.ServerError as e:
            wait = 2 ** attempt
            print(f"[재시도 {attempt + 1} / {max_retries}] {wait}초 대기...")
            time.sleep(wait)
    raise RuntimeError(f"{max_retries}회 재시도 모두 실패")


response = safe_generate(client=client, model="gemini-2.5-flash", contents=text, config=config, max_retries=3)
print(response.text)
print("=== 토큰 사용량 ===")
print(f"입력:           {response.usage_metadata.prompt_token_count}")
print(f"출력:           {response.usage_metadata.candidates_token_count}")
print(f"추론(thinking): {response.usage_metadata.thoughts_token_count}")
print(f"합계:           {response.usage_metadata.total_token_count}")