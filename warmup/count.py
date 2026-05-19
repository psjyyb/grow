filename = "hello.txt"

with open(file=filename, mode="r", encoding="utf-8") as f:
    text = f.read()

line_count = len(text.splitlines())
char_count = len(text)
print(f"파일: {filename}")
print(f"- 줄 수: {line_count}")
print(f"- 글자 수: {char_count}")

# 커밋 테스트