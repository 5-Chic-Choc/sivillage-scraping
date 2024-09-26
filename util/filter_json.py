import json

# 원본 JSON 데이터를 읽어옵니다
with open('../product_sizes.json', 'r', encoding='utf-8') as file:
    product_main = json.load(file)

# 사용하는 필드들만 남기기 위한 함수
def filter_used_fields(product):
    return {
        "size": product.get("size_value"),
    }

# 새로운 데이터를 생성
filtered_colors = [filter_used_fields(product) for product in product_main]

# 필터링한 데이터를 새로운 JSON 파일로 저장
with open('../merged_data/sizes.json', 'w', encoding='utf-8') as outfile:
    json.dump(filtered_colors, outfile, ensure_ascii=False, indent=4)

print("필터링된 JSON 파일이 생성되었습니다.")