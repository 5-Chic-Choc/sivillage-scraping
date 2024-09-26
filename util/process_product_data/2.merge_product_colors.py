import json

# JSON 파일 읽기
with open('../merged_data/products.json', 'r', encoding='utf-8') as filtered_file:
  filtered_products = json.load(filtered_file)

with open('../product_colors.json', 'r', encoding='utf-8') as colors_file:
  product_colors = json.load(colors_file)

# 색상 값을 리스트로 저장하기 위한 매핑 작업
# 먼저 product_code 기준으로 color_value를 리스트에 저장
color_map = {}

for color in product_colors:
  product_code = color['product_code']
  color_value = color['color_value']

  if product_code in color_map:
    color_map[product_code].append(color_value)  # 이미 있는 경우 리스트에 추가
  else:
    color_map[product_code] = [color_value]  # 처음 등장하는 product_code는 리스트로 초기화

# filtered_products에 color_value 추가 (리스트 형태로)
for product in filtered_products:
  goods_no = product.get('goods_no')
  # product_code가 goods_no와 매칭되면 color_value 리스트 추가
  product['color_values'] = color_map.get(goods_no, [])  # 매칭 안 되면 빈 리스트

# 결과를 새로운 JSON 파일로 저장
with open('../merged_data/2.filtered_product_info_with_colors.json', 'w',
          encoding='utf-8') as output_file:
  json.dump(filtered_products, output_file, ensure_ascii=False, indent=4)

print("여러 개의 색상 정보가 추가된 filtered_product_info_with_colors.json 파일이 생성되었습니다.")