import json

# 원본 JSON 데이터를 읽어옵니다
with open('../product_main.json', 'r', encoding='utf-8') as file:
    product_main = json.load(file)

# 사용하는 필드들만 남기기 위한 함수
def filter_used_fields(product):
    return {
        "goods_no": product.get("goods_no"),
        "goods_nm": product.get("goods_nm"),
        "brand_nm": product.get("brand_nm"),
        "disp_lctg_nm": product.get("disp_lctg_nm"),
        "disp_mctg_nm": product.get("disp_mctg_nm"),
        "disp_sctg_nm": product.get("disp_sctg_nm"),
        "disp_dctg_nm": product.get("disp_dctg_nm"),
        "normal_price": product.get("normal_price"),
        "discount_price": product.get("general_cust_sale_price")
    }

# 새로운 데이터를 생성
filtered_products = [filter_used_fields(product) for product in product_main]

# 필터링한 데이터를 새로운 JSON 파일로 저장
with open('../merged_data/1.filtered_product_info.json', 'w', encoding='utf-8') as outfile:
    json.dump(filtered_products, outfile, ensure_ascii=False, indent=4)

print("필터링된 JSON 파일이 생성되었습니다.")