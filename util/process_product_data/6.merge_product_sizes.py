import json

# JSON 파일 읽기
with open('../merged_data/5.product_main_with_images.json', 'r', encoding='utf-8') as main_file:
  product_main = json.load(main_file)

with open('../product_sizes.json', 'r', encoding='utf-8') as sizes_file:
  product_sizes = json.load(sizes_file)

# 사이즈 정보를 딕셔너리 형태로 저장 (product_code 기준으로 size_value를 저장)
size_map = {}

for size_data in product_sizes:
  product_code = size_data['product_code']
  size_value = size_data['size_value']

  # 동일한 product_code에 여러 사이즈가 있을 수 있으므로 딕셔너리로 리스트 관리
  if product_code in size_map:
    size_map[product_code].append(size_value)
  else:
    size_map[product_code] = [size_value]  # 처음 등장한 경우 리스트로 초기화

# product_main에 사이즈 리스트 추가
for product in product_main:
  goods_no = product.get('goods_no')
  # goods_no와 매칭되는 product_code에서 사이즈 리스트 추가
  product['sizes'] = size_map.get(goods_no, [])  # 매칭 안 되면 빈 리스트

# 결과를 새로운 JSON 파일로 저장
with open('../merged_data/6.product_main_with_sizes.json', 'w', encoding='utf-8') as output_file:
  json.dump(product_main, output_file, ensure_ascii=False, indent=4)

print("사이즈 정보가 추가된 product_main_with_sizes.json 파일이 생성되었습니다.")