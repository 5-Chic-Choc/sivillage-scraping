from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Chrome 드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 페이지 열기
driver.get('https://www.sivillage.com/event/initEventMain.siv?gnb_class=event')

# 페이지 로드 대기
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'event__content-list')))

# 각 페이지에서 데이터를 저장할 리스트
all_items = []


def parse_event_list():
  # 현재 페이지의 HTML을 BeautifulSoup로 파싱
  soup = BeautifulSoup(driver.page_source, 'html.parser')
  ul_element = soup.find('ul', class_='event__content-list')
  if ul_element:
    li_elements = ul_element.find_all('li', class_='event__content-item')
    for li in li_elements:
      # 필요한 정보를 추출
      a_tag = li.find('a')
      if a_tag and 'href' in a_tag.attrs:
        href_content = a_tag['href']

        # PLANSHOPDTL, EVENTDTL, 일반 URL 세 가지 경우 처리
        if 'PLANSHOPDTL' in href_content:
          href_split = href_content.split("'")
          disp_ctg_no = href_split[3]
          event_type = "brandEvent"
        elif 'EVENTDTL' in href_content:
          href_split = href_content.split("'")
          event_no = href_split[3]
          event_type = "mallEvent"
        else:
          # 일반 URL에서 event_no를 추출
          event_no = href_content.split('event_no=')[
            1] if 'event_no=' in href_content else None
          event_type = "affiliation"

        # 공통된 이미지 태그 처리
        img_tag = li.find('img')['src']

        # 제목과 태그 처리
        # PLANSHOPDTL과 EVENTDTL에 따라 다른 p 태그 가져오기
        small_title_tag = li.find('p',
                                  class_='event__content-item-text-small-title')
        box_tag = li.find('p', class_='event__content-item-text-box')

        # PLANSHOPDTL의 경우 event__content-item-text-small-title 사용
        if small_title_tag and small_title_tag.get_text(strip=True):
          title = li.find('p',
                          class_='event__content-item-text-title').get_text(
            strip=True)
          brand = small_title_tag.find('span').get_text(
            strip=True) if small_title_tag.find('span') else ''
        # EVENTDTL의 경우 event__content-item-text-box 사용
        elif box_tag:
          title = li.find('p',
                          class_='event__content-item-text-title').get_text(
            strip=True)
          brand = box_tag.get_text(strip=True)
        # 일반 URL 형태 처리 (brand 없이)
        else:
          title = li.find('p',
                          class_='event__content-item-text-title').get_text(
            strip=True)
          brand = ''  # 브랜드 정보가 없을 경우 빈 문자열로 처리

        # 설명 처리
        description = li.find('p',
                              class_='event__content-item-text-description').get_text(
          strip=True)

        # Tags 처리 - 단일 태그 또는 여러 개의 태그 처리
        tag_element = li.find('p', class_='event__content-item-text-tag')
        if tag_element:
          # 문자열 내 불필요한 공백, 탭, 줄바꿈 제거 후 배열로 변환
          tags_raw = tag_element.get_text(separator=' ').strip()
          # 태그가 단 하나일 경우와 다수일 경우 모두 처리
          tags = [tag.strip() for tag in tags_raw.split() if tag.strip()]
        else:
          tags = []  # 태그가 없을 경우 빈 리스트

        # 결과 저장
        item = {
          'id': disp_ctg_no if 'PLANSHOPDTL' in href_content else event_no,
          'type': event_type,
          'thumbnail_img': img_tag,
          'brand': brand,
          'title': title,
          'description': description,
          'tags': tags
        }

        all_items.append(item)


# 첫 번째 페이지 파싱
parse_event_list()

# 페이지네이션 처리 - 페이지 번호를 직접 클릭
for page_num in range(9, 11):
  try:
    # 페이지 번호를 직접 선택
    page_button = driver.find_element(By.XPATH,
                                      f"//a[@class='siv-pagination__btn' and text()='{page_num}']")
    page_button.click()
    time.sleep(5)  # 페이지가 완전히 로드될 시간을 주기 위해 sleep 추가

    # 새로운 페이지에서 다시 event__content-list가 로드될 때까지 기다림
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'event__content-list')))

    # 새 페이지의 리스트를 파싱
    parse_event_list()
  except Exception as e:
    print(f"Error occurred on page {page_num}: {e}")
    break

# 브라우저 종료
# driver.quit()

# 결과 출력
import json

print(json.dumps(all_items, ensure_ascii=False, indent=4))

# 결과를 파일로 저장 (JSON 파일)
with open('eventlist0918_2.json', 'w', encoding='utf-8') as f:
  json.dump(all_items, f, ensure_ascii=False, indent=4)
