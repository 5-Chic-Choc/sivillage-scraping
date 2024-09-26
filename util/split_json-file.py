import json
import os

def count_json_objects(json_file):
  # JSON 파일 열기
  with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

  # 객체 수 계산
  return len(data)

def split_json_file(file_path, split_count):
  # 원본 파일 이름과 확장자 분리
  base_name, ext = os.path.splitext(os.path.basename(file_path))

  # JSON 파일 열기
  with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

  # 데이터 객체 갯수
  total_objects = len(data)
  print(f"전체 객체 수: {total_objects}")

  # 분할할 크기 계산
  chunk_size = total_objects // split_count
  remainder = total_objects % split_count

  # 폴더 생성 (기존 파일 이름으로)
  output_dir = base_name
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"폴더 생성: {output_dir}")

  start_index = 0
  for i in range(1, split_count + 1):
    # 나머지 처리: 각 분할 파일이 한 개의 객체를 더 가질 수 있도록 분배
    end_index = start_index + chunk_size + (1 if remainder > 0 else 0)
    chunk = data[start_index:end_index]

    # 나머지를 감소시킴
    if remainder > 0:
      remainder -= 1

    # 새로운 파일 이름
    new_file_path = os.path.join(output_dir, f"{base_name}_{i}{ext}")

    # 분할된 데이터를 새로운 JSON 파일로 저장
    with open(new_file_path, 'w', encoding='utf-8') as new_file:
      json.dump(chunk, new_file, ensure_ascii=False, indent=4)

    print(f"저장된 파일: {new_file_path} (객체 수: {len(chunk)})")

    start_index = end_index


if __name__ == "__main__":
  # !!!!!!!!!!!! 여기서 대상 파일 수정 !!!!!!!
  file_path = "./data/brandEvent/brand_events_0918_no_product_info.json"

  object_count = count_json_objects(file_path)
  print(f"JSON 파일 내 객체 수: {object_count}")

  split_count = int(input("분할할 파일 갯수를 입력하세요: "))

  split_json_file(file_path, split_count)
