x = 42

fruits = ["사과", "바나나", "포도"]
fruits.append("키위")          # 끝에 추가  (Java: list.add())
fruits[0]                       # "사과"      (인덱스 0부터)
fruits[-1]                      # "키위"      (음수 인덱스 = 뒤에서부터)
len(fruits)

nums = [10, 20, 30, 40, 50]
nums[1:4]        # [20, 30, 40]  (인덱스 1부터 4 바로 전까지)
nums[:3]         # [10, 20, 30]  (처음부터 3 바로 전까지)
nums[-2:]

user = {"name": "kim", "age": 30}
user["name"]                    # "kim"            (Java: map.get("name"))
user["email"] = "k@x.com"       # 추가/덮어쓰기      (Java: map.put())
del user["age"]                 # 삭제             (Java: map.remove())
"name" in user


age = 1
if age > 65:
    grade = "노인"
elif age < 35:
    grade = "중년"
else:
    grade = "청년"

result = "노인" if age > 65 else "청년"

#for i in range(5):


#for fruit in fruits:
    #print(fruit)
    #if fruit == "사과":
        #print("즙")

# for i, fruit in enumerate(fruits):
#     print(f"{i}: {fruit}")

# for n in range(10):
#     if n == 9:
#         break        # 반복 즉시 종료
#     if n == 2:
#         continue     # 이번 회차 건너뛰고 다음으로
#     print(n)

def add(a: int, b: int):
    return a + b
#print(add(1,2))

def greet(name: str, message: str = "하이요" ):
    print(f"{message}, {name}")
#greet(name="Zohn", message="나의 이름은")

nums = [3, 1, 4, 1, 5, 9, 2, 6]
tot = 0
for num in nums:
    if num % 2 == 0:
        tot += num
print(f"짝수 합: {tot}")

price = 1234567
#print(f"가격: {price:,}원")        # "가격: 1,234,567원" (천 단위 콤마)
#print(f"파이: {3.14159:.2f}")