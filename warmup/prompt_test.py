from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")

client=genai.Client(api_key=api_key) # 환경변수에서 가져온 키 값 인자로 넘기기


config=types.GenerateContentConfig(
    system_instruction="""너는 한국어 자기소개에서 정보를 추출한다.
    답은 반드시 JSON으로만 출력. 키는 name, age, city. 모르는 값은 null.""",
    response_mime_type="application/json"

)
response=client.models.generate_content(
    model="gemini-2.5-flash",
    config=config,
    contents="안녕하세요, 저는 김철수입니다. 서울 사는 35살 직장인이에요."
)
print(response.text)

data=json.loads(response.text)
print(data["name"])
print(data["age"])