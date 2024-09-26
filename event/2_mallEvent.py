from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from PIL import Image
import requests
from io import BytesIO
import time

# Chrome 드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 파일에서 mallEvent인 데이터를 필터링
import json

with open('eventlist0918_1.json', 'r', encoding='utf-8') as f:
  data = json.load(f)

mall_events = [item for item in data if item['type'] == 'mallEvent']


# 이미지 크기 확인하는 함수 (width, height로 필터링)
def is_valid_image(image_url, min_width=500, min_height=300):
  try:
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    width, height = img.size
    return width >= min_width and height >= min_height
  except Exception as e:
    print(f"Error checking image {image_url}: {e}")
    return False


# 최대 3개의 유효한 이미지 추출하는 함수
def get_event_images(event_id):
  event_url = f"https://m.sivillage.com/event/initEventDetail.siv?event_no={event_id}"
  driver.get(event_url)
  time.sleep(3)  # 페이지 로드 대기

  soup = BeautifulSoup(driver.page_source, 'html.parser')

  # 최대 3개의 유효한 이미지 추출
  images = []
  promotion_divs = soup.find_all('div', class_='promotion')
  for promotion in promotion_divs:
    img_tags = promotion.find_all('img')
    for img in img_tags:
      if 'promotion' in promotion.get('class', []) and 'src' in img.attrs:
        img_url = img['src']
        # 이미지 크기 확인 후 추가
        if is_valid_image(img_url):
          images.append(img_url)
      if len(images) >= 3:
        break
    if len(images) >= 3:
      break
  return images


# mallEvent 유형의 각 이벤트에 대해 이미지 추출
for event in mall_events:
  event_id = event['id']
  event_images = get_event_images(event_id)
  event['promotion_images'] = event_images

# 결과를 파일로 저장
with open('mall_events_with_images_size.json', 'w', encoding='utf-8') as f:
  json.dump(mall_events, f, ensure_ascii=False, indent=4)

# 드라이버 종료
driver.quit()