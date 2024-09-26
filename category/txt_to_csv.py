import csv

# 입력된 계층형 텍스트를 CSV로 변환하는 함수
def parse_lines_to_hierarchy(lines):
    result = []
    stack = []  # (id, level) 형태로 부모 ID와 들여쓰기 레벨을 추적
    current_id = 1  # ID 값 초기화

    for line in lines:
        stripped_line = line.strip().lstrip('- ')  # '- ' 부분 제거
        indent_level = (len(line) - len(line.lstrip())) // 4  # 들여쓰기 레벨 계산

        # 현재 노드의 부모를 찾기 위해 스택에서 적절한 레벨로 이동
        while stack and stack[-1][1] >= indent_level:
            stack.pop()

        # 부모 ID는 스택의 마지막 항목의 ID (상위 레벨) 또는 None (최상위 항목일 경우)
        parent_id = stack[-1][0] if stack else None

        # 노드의 정보를 기록
        node = {
            "id": current_id,
            "name": stripped_line,
            "parent_id": parent_id,
            "level": indent_level
        }
        result.append(node)

        # 현재 노드를 스택에 추가 (id, level)
        stack.append((current_id, indent_level))

        current_id += 1  # ID 증가

    return result

# 텍스트 파일을 읽어 CSV로 변환하는 함수
def convert_txt_to_csv(txt_file_path, csv_file_path):
    # 텍스트 파일을 읽어옴
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 계층형 데이터를 파싱하여 결과를 얻음
    hierarchy = parse_lines_to_hierarchy(lines)

    # CSV 파일로 저장
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'name', 'parent_id', 'level']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for node in hierarchy:
            writer.writerow(node)

    print(f"CSV 파일이 {csv_file_path}로 저장되었습니다.")

# 경로 설정
txt_file_path = 'categorymd.txt'  # 텍스트 파일 경로
csv_file_path = 'category_output.csv'  # 생성될 CSV 파일 경로

# 함수 호출
convert_txt_to_csv(txt_file_path, csv_file_path)