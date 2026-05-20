import sqlite3
import os

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

con = sqlite3.connect("sample.db")
cur = con.cursor()
cur.execute("SELECT sql FROM sqlite_master WHERE type='table'")
schemas = "\n\n".join(row[0] for row in cur.fetchall())
con.close()

question = "고래밥을 구매한 고객 이름"
system_instruction = f"""너는 SQLite SQL 전문가다.
사용자의 자연어 질문을 다음 DB 에 대한 SELECT 쿼리로 변환한다.

[스키마]
{schemas}

[테이블 관계]
- orders.customer_id 는 customers.customer_id 를 참조 (구매자)
- orders.product_id 는 products.product_id 를 참조 (구매 상품)
- 매출 = products.price × orders.quantity

[규칙]
- SQLite 문법 사용
- SELECT 만 허용 (DROP/DELETE/UPDATE/INSERT 절대 금지)
- 코드 블록(```) 표시 없이 SQL 문장만 출력
- 다른 인사말, 설명, 주석 금지
- 테이블 alias 는 의미 있게 사용 (c=customers, o=orders, p=products)

[예시]
질문: 서울 거주 고객 이름
SQL: SELECT name FROM customers WHERE city = '서울';

질문: 카테고리별 총 매출
SQL: SELECT p.category, SUM(p.price * o.quantity) AS total
     FROM orders o JOIN products p ON o.product_id = p.product_id
     GROUP BY p.category;
"""

config = types.GenerateContentConfig(
    system_instruction = system_instruction
)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=config,
    contents=question
)

print(response.text)
