import os
import time
from google import genai
from dotenv import load_dotenv
from google.genai import errors

load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def safe_generate(client, model, contents, max_retries=3):
    """503 같은 일시 오류 만나면 자동 재시도"""
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model=model,
                contents=contents
            )
        except errors.ServerError as e:
            wait=2 ** attempt
            print(f"[재시도 {attempt+1}/{max_retries}] {wait}초 대기...")
            time.sleep(wait)
    raise RuntimeError(f"{max_retries}회 재시도 모두 실패")

response=safe_generate(client=client, model="gemini-2.5-flash", contents="안녕이라고 말하지마", max_retries=3)
print(response.text)