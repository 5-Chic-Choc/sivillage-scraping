import json

# 예시 데이터


# JSON 파일 경로
with open('../merged_data/sizes.json', 'r', encoding='utf-8') as file:
  size_data =  json.load(file)


# 중복 제거 및 하나의 리스트로 변환
unique_sizes = list({item['size'] for item in size_data})

# 딕셔너리 형태로 변환
result = {'sizes': unique_sizes}

# JSON 문자열로 변환하여 출력
json_result = json.dumps(result, ensure_ascii=False, indent=4)
print(json_result)