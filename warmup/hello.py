from google import genai
from dotenv import load_dotenv
import os # 표준 라이브러리, 환경변수 읽기용

load_dotenv() # 인자 없이 호출하면 현재 폴더의 .env를 자동으로 찾아서 환경변수로 등록
api_key = os.getenv("GEMINI_API_KEY") # 환경변수에서 가져온 값 변수에 담아두기

client = genai.Client(api_key=api_key) # 환경변수에서 가져온 키 값 인자로 넘기기

response = client.models.generate_content(model="gemini-2.5-flash", contents="서울의 오늘 날씨를 한국어로 답해주세요.")

print(response.text)
