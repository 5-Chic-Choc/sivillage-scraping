from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json

# Chrome 드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 파일에서 affiliation 데이터를 필터링
with open('eventlist0918_1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# affiliation 타입만 필터링
affiliation_events = [item for item in data if item['type'] == 'affiliation']


# 이벤트 상세 페이지에서 이미지 URL 추출 함수
def get_affiliation_event_images(event_id):
    # 이벤트 상세 페이지 URL 생성
    event_url = f"https://www.sivillage.com/event/initEventDetail.siv?event_no={event_id}"

    # 페이지 로드
    driver.get(event_url)
    time.sleep(2)  # 페이지 로드 대기

    # BeautifulSoup으로 페이지 파싱
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # div.event-detail__html 내의 이미지 태그 찾기
    event_images = []
    event_html_div = soup.find('div', class_='event-detail__html')
    if event_html_div:
        img_tags = event_html_div.find_all('img')
        for img_tag in img_tags:
            img_src = img_tag['src']
            event_images.append(img_src)

    return event_images


# 메인 함수
def process_affiliation_event(event, idx):
    print(f"Processing affiliation event {idx + 1} of {len(affiliation_events)}")

    # 이벤트 id 가져오기
    event_id = event['id']

    # 이벤트 상세 페이지에서 이미지 추출
    event_images = get_affiliation_event_images(event_id)

    # 결과 저장
    event['event_images'] = event_images


# affiliation 이벤트 처리
for idx, event in enumerate(affiliation_events):
    process_affiliation_event(event, idx)

# 결과를 파일로 저장
with open('affiliation_events_with_images.json', 'w', encoding='utf-8') as f:
    json.dump(affiliation_events, f, ensure_ascii=False, indent=4)

# 드라이버 종료
driver.quit()