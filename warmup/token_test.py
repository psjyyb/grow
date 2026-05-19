from google import genai
from dotenv import load_dotenv
import os
from google.genai import errors

load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

texts=[
    "안녕하세요. 오늘 날씨가 좋네요.",
    "Hello. The weather is nice today.",
    "What should we have for lunch?",
    "Python의 리스트는 순서가 있고 변경 가능한 자료구조입니다",
    "Python's list is an ordered and mutable data structure"
]

# for text in texts:
#     result  = client.models.count_tokens(
#         model="gemini-2.5-flash",
#         contents=text
#     )
#     print(f"{result.total_tokens:3d} 토큰 | {text}")

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="파이썬의 list를 한 줄로 설명해줘"
    )
except errors.ServerError as e:
    print(f"서버 오류: {e}")
except errors.ClientError as e:
    print(f"내 요청에 문제 있음, 코드 점검: {e}")
except Exception as e:
    print(f"예상 못한 오류: {e}")

print("답변:", response.text)
print("=== 토큰 사용량 ===")
print(f"입력:           {response.usage_metadata.prompt_token_count}")
print(f"출력:           {response.usage_metadata.candidates_token_count}")
print(f"추론(thinking): {response.usage_metadata.thoughts_token_count}")
print(f"합계:           {response.usage_metadata.total_token_count}")