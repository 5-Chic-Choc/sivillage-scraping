import json


# JSON 파일의 객체 수를 구하는 함수
def count_json_objects(json_file):
  # JSON 파일 열기
  with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

  # 객체 수 계산
  return len(data)


# JSON 파일의 객체 수 출력
json_file = 'data/brandEvent/forme/brand_events_0918_no_product_info.json'
object_count = count_json_objects(json_file)
print(f"JSON 파일 내 객체 수: {object_count}")