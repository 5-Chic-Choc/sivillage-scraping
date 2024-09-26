import json

# JSON 파일 읽기
with open('../merged_data/2.filtered_product_info_with_colors.json', 'r', encoding='utf-8') as main_file:
    product_main = json.load(main_file)

with open('../product_detail_iframe.json', 'r', encoding='utf-8') as iframe_file:
    product_iframe = json.load(iframe_file)

# iframe 정보를 저장할 딕셔너리 (product_code 기준으로 src 값 저장)
iframe_map = {iframe['product_code']: iframe['src'] for iframe in product_iframe}

# product_main에 src 추가
for product in product_main:
    goods_no = product.get('goods_no')
    # goods_no와 매칭되는 product_code에서 src 값을 가져와 추가
    product['src'] = iframe_map.get(goods_no, "")  # 매칭 안 되는 경우 빈 값("")

# 결과를 새로운 JSON 파일로 저장
with open('../merged_data/3.product_main_with_iframe.json', 'w', encoding='utf-8') as output_file:
    json.dump(product_main, output_file, ensure_ascii=False, indent=4)

print("iframe 정보가 추가된 product_main_with_iframe.json 파일이 생성되었습니다.")