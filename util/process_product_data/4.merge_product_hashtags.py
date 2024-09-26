import json

# JSON 파일 읽기
with open('../merged_data/3.product_main_with_iframe.json', 'r', encoding='utf-8') as main_file:
  product_main = json.load(main_file)

with open('../product_hashtags.json', 'r', encoding='utf-8') as hashtags_file:
  product_hashtags = json.load(hashtags_file)

# 해시태그 정보를 딕셔너리 형태로 저장 (product_code 기준으로 hashtag를 저장)
hashtag_map = {}

for hashtag_data in product_hashtags:
  product_code = hashtag_data['product_code']
  hashtag = hashtag_data['hashtag']

  # 동일한 product_code에 여러 해시태그가 있을 수 있으므로 딕셔너리로 관리
  if product_code in hashtag_map:
    hashtag_map[product_code].append(hashtag)
  else:
    hashtag_map[product_code] = [hashtag]  # 처음 등장한 경우 리스트로 초기화

# product_main에 hashtag 딕셔너리 추가
for product in product_main:
  goods_no = product.get('goods_no')
  # goods_no와 매칭되는 product_code에서 해시태그 리스트 추가
  product['hashtags'] = hashtag_map.get(goods_no, {})  # 매칭 안 되는 경우 빈 딕셔너리

# 결과를 새로운 JSON 파일로 저장
with open('../merged_data/4.product_main_with_hashtags.json', 'w',
          encoding='utf-8') as output_file:
  json.dump(product_main, output_file, ensure_ascii=False, indent=4)

print("해시태그 정보가 추가된 product_main_with_hashtags.json 파일이 생성되었습니다.")