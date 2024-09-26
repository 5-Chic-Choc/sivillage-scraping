import json

# JSON 파일 읽기
with open('../merged_data/4.product_main_with_hashtags.json', 'r', encoding='utf-8') as main_file:
  product_main = json.load(main_file)

with open('../product_images.json', 'r', encoding='utf-8') as images_file:
  product_images = json.load(images_file)

# 이미지 정보를 딕셔너리 형태로 저장 (product_code 기준으로 idx, src 값을 저장)
image_map = {}

for image_data in product_images:
  product_code = image_data['product_code']
  idx = image_data['idx']
  src = image_data['src']

  # 동일한 product_code에 여러 이미지가 있을 수 있으므로 딕셔너리로 리스트 관리
  if product_code in image_map:
    image_map[product_code].append({"idx": idx, "src": src})
  else:
    image_map[product_code] = [{"idx": idx, "src": src}]  # 처음 등장한 경우 리스트로 초기화

# product_main에 이미지 리스트 추가
for product in product_main:
  goods_no = product.get('goods_no')
  # goods_no와 매칭되는 product_code에서 이미지 리스트 추가
  product['images'] = image_map.get(goods_no, [])  # 매칭 안 되면 빈 리스트

# 결과를 새로운 JSON 파일로 저장
with open('../merged_data/5.product_main_with_images.json', 'w',
          encoding='utf-8') as output_file:
  json.dump(product_main, output_file, ensure_ascii=False, indent=4)

print("이미지 정보가 추가된 product_main_with_images.json 파일이 생성되었습니다.")