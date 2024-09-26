import csv
import pymysql

# MySQL 데이터베이스에 연결하는 함수
def connect_to_db(host, user, password, database, port):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# CSV 데이터를 MySQL 데이터베이스에 삽입하는 함수
def insert_csv_to_db(csv_file_path, db_connection):
    try:
        with db_connection.cursor() as cursor:
            # CSV 파일 읽기
            with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                # 데이터 삽입 쿼리 준비
                sql = """
                INSERT INTO category (depth, category_id, parent_id, name )
                VALUES (%s, %s, %s, %s)
                """

                for row in reader:
                    # parent_id가 빈 문자열일 경우 None으로 처리
                    parent_id = row['parent_id'] if row['parent_id'] else None

                    # 데이터 삽입
                    cursor.execute(sql, (row['depth'], row['category_id'], parent_id, row['name']))

            # 변경 사항 커밋
            db_connection.commit()
            print("CSV 데이터를 성공적으로 삽입했습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        db_connection.close()

# 실행 부분
if __name__ == "__main__":
    # 사용자 입력 (포트와 비밀번호를 직접 입력하세요)
    host = '43.201.30.206'  # 예: 'localhost'
    user = 'root'  # 예: 'root'
    password = 'chicchoc@2024'  # 사용자 입력
    database = 'chicchoc_siv_db'
    port = 3306  # 예: 3306

    # CSV 파일 경로
    csv_file_path = 'category_output.csv'  # CSV 파일 경로

    # MySQL에 연결
    db_connection = connect_to_db(host, user, password, database, port)

    # CSV 데이터를 MySQL에 삽입
    insert_csv_to_db(csv_file_path, db_connection)