import sqlite3
import os
import sys
import time
from google import genai
from google.genai import types
from google.genai import errors
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

con = sqlite3.connect("sample.db")
cur = con.cursor()
cur.execute("SELECT sql FROM sqlite_master WHERE type='table'")
schemas = "\n\n".join(row[0] for row in cur.fetchall())
con.close()

question = "고객의 나이"
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
def safe_generate(client, model, contents, config, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model=model,
                contents=contents,
                config=config
            )
        except errors.ServerError as e:
            wait = 2 ** attempt
            print(f"[재시도 {attempt + 1} / {max_retries}] {wait}초 대기...")
            time.sleep(wait)
    raise RuntimeError(f"{max_retries}회 재시도 모두 실패")

response = safe_generate(client=client, model="gemini-2.5-flash", config=config, contents=question)

sql = response.text.strip()
if sql.startswith("```"):
    lines = sql.split("\n")
    lines = [ln for ln in lines if not ln.strip().startswith("```")]
    sql = "\n".join(lines).strip()

if not sql.lower().startswith("select"):
    print(f"위험한 SQL 거부: \n{sql}")
    sys.exit(1)

con = sqlite3.connect("sample.db")
cur = con.cursor()
try:
    cur.execute(sql)
    rows = cur.fetchall()
    headers = [desc[0] for desc in cur.description]
    con.close()

    print("=== 결과 ===")
    print(tabulate(rows, headers=headers, tablefmt="grid"))
except sqlite3.Error as e:
    error_message = str(e)
    failed_sql = sql
    print(f"[1차 실패] {error_message}")

    retry_message = f"""원래 질문: {question}
    이전에 시도한 SQL: {failed_sql}
    실행 시 에러: {error_message}
    위 에러를 분석해서 수정된 SQL만 출력해줘.
    """
    response = safe_generate(client=client, model="gemini-2.5-flash", config=config, contents=retry_message)
    sql2 = response.text.strip()
    if sql2.startswith("```"):
        lines = sql2.split("\n")
        lines = [ln for ln in lines if not ln.strip().startswith("```")]
        sql2 = "\n".join(lines).strip()
    if not sql.lower().startswith("select"):
        print(f"위험 SQL 거부:\n{sql2}")
        sys.exit(1)
    con2 = sqlite3.connect("sample.db")
    cur2 = con2.cursor()
    cur2.execute(sql2)
    rows = cur2.fetchall()
    headers = [desc[0] for desc in cur2.description]
    con2.close()

    print("=== 재시도 SQL ===")
    print(sql2)
    print("=== 재시도 결과 ===")
    print(tabulate(rows, headers=headers, tablefmt="grid"))