import sqlite3
import os

if os.path.exists("sample.db"):
    os.remove("sample.db")
con = sqlite3.connect("sample.db")
cur = con.cursor()
cur.execute("""
    CREATE TABLE customers
    (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT NOT NULL, -- 고객 이름(실명)
        city        TEXT, -- 거주 도시 (서울/부산/대구등 지역명)
        signup_date TEXT -- 가입일 (YYYY-MM-DD)
    )
""")
cur.execute("""
    CREATE TABLE products
    (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, -- 상품명
        category TEXT, -- 카테고리 (과자/도서/전자...)
        price INTEGER, -- 단가(원)
        add_date TEXT -- 상품 등록일(YYYY-MM-DD)
    )
""")
cur.execute("""
    CREATE TABLE orders
    (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL, -- 구매 상품(products.product_id 참조)
        order_date TEXT NOT NULL, -- 주문일(YYYY-MM-DD)
        customer_id INTEGER NOT NULL, -- 구매자 (customers.customer_id 참조)
        quantity INTEGER NOT NULL -- 주문 수량
    )
""")
customer_data = [
    ("김철수", "서울", "2025-03-15"),
    ("이옥자", "부산", "2024-03-12"),
    ("이옥춘", "광주", "2024-03-15"),
    ("양성룡", "대구", "2026-04-12"),
    ("박유룡", "대구", "2026-04-12"),
]
cur.executemany("INSERT INTO customers (name, city, signup_date) VALUES (?, ?, ?)", customer_data)
products_data = [
    ("고래밥", "과자", 1500, "2026-05-10"),
    ("젤리의 연금술", "도서", 18000, "2026-05-12"),
    ("새우깡", "과자", 1300, "2026-05-13"),
    ("무선 키보드", "전자", 45000, "2026-05-14"),
    ("Python 입문", "도서", 22000, "2026-05-15"),
]
cur.executemany("INSERT INTO products (name, category, price, add_date) VALUES (?, ?, ?, ?)", products_data)
order_data = [
    (4, 1, 3, "2026-05-19"),  # 양성룡, 고래밥 3개
    (5, 1, 2, "2026-05-19"),  # 박유룡, 고래밥 2개
    (1, 2, 1, "2026-05-15"),  # 김철수, 젤리의 연금술 1개
    (1, 4, 1, "2026-04-28"),  # 김철수, 키보드 1개
    (2, 3, 5, "2026-05-10"),  # 이옥자, 새우깡 5개
    (2, 5, 1, "2026-05-12"),  # 이옥자, Python 입문 1개
    (3, 2, 2, "2026-04-05"),  # 이옥춘, 젤리의 연금술 2개
    (4, 5, 1, "2026-05-01"),  # 양성룡, Python 입문 1개
]
cur.executemany("INSERT INTO orders (customer_id, quantity, product_id, order_date) VALUES (?, ?, ?, ?)", order_data)

con.commit()
print("DB 생성 완료: sample.db")
#for row in cur.execute("SELECT c.name, p.name, o.order_date FROM orders o LEFT OUTER JOIN customers c ON o.customer_id = c.customer_id LEFT OUTER JOIN products p ON o.product_id = p.product_id"):
for row in cur.execute("SELECT city FROM customers"):
    print()
con.close()
