from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from PIL import Image
import requests
from io import BytesIO
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# Chrome 드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 파일에서 brandEvent 데이터를 필터링 (최대 10개)
with open('eventlist0918_2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 최대 10개의 brandEvent만 처리
brand_events = [item for item in data if item['type'] == 'brandEvent'][:50]


# 이미지 크기 확인 함수
def is_valid_image(image_url, min_width=600, min_height=400):
    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        width, height = img.size
        return width >= min_width and height >= min_height
    except Exception as e:
        print(f"Error checking image {image_url}: {e}")
        return False


# 쿠폰 정보 추출 함수
def get_coupon_info(soup):
    coupon = {}
    coupon_div = soup.find('div', class_='event-detail__coupon')
    if coupon_div:
        name = coupon_div.find('p', class_='event-detail__coupon-text info-name').get_text(strip=True)
        discount = coupon_div.find('p', class_='event-detail__coupon-text discount').get_text(strip=True)
        period = coupon_div.find('p', class_='event-detail__coupon-text period').find('span', class_='coupon-term').get_text(strip=True)
        coupon_kind = coupon_div.find('p', class_='event-detail__coupon-text period').find('span', class_='coupon-kinds').get_text(strip=True)

        coupon = {
            'name': name,
            'discount': discount,
            'period': period,
            'kind': coupon_kind
        }

    return coupon

# 카테고리별 상품 정보 추출 함수 (최대 15개로 제한)
def get_category_products(category_link):
    driver.get(category_link)
    time.sleep(2)  # 페이지 로드 대기
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    product_list = []
    product_items = soup.find_all('li', class_='product__item')

    # 최대 15개의 상품만 수집
    for idx, product in enumerate(product_items):
        if idx >= 20:
            break  # 15개까지만 처리

        # goods_no 수집 (onclick 속성에서 추출)
        onclick_attr = product.find('a', class_='product__data')['onclick']
        goods_no = onclick_attr.split("goods_no : '")[1].split("'")[0]

        name = product.find('p', class_='product__data-name').get_text(strip=True)

        product_list.append({
            'goods_no': goods_no,
            'name': name
        })

    return product_list


# Tab 카테고리 클릭 처리 함수
def click_tab_category():
    category_div = driver.find_element(By.CLASS_NAME, 'event-separator-tab')
    category_links = category_div.find_elements(By.TAG_NAME, 'a')
    categories = []
    category_urls = []

    # 카테고리 클릭하고 URL 저장
    for category_link in category_links:
        category_name = category_link.text
        categories.append(category_name)

        # 클릭이 가능할 때까지 기다림
        WebDriverWait(driver, 1).until(EC.element_to_be_clickable(category_link))

        # JavaScript로 클릭
        driver.execute_script("arguments[0].click();", category_link)

        time.sleep(1)  # 페이지가 로드될 시간을 대기
        category_urls.append(driver.current_url)

    return categories, category_urls


# Selectbox 카테고리 클릭 처리 함수
def click_selectbox_category():
    selectbox_div = driver.find_element(By.CLASS_NAME, 'siv-selectbox')
    selectbox_button = selectbox_div.find_element(By.CLASS_NAME, 'selected')

    driver.execute_script("arguments[0].scrollIntoView(true);", selectbox_button)
    driver.execute_script("arguments[0].click();", selectbox_button)

    WebDriverWait(driver, 1).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.selectbox-wrap[style='display: block;']"))
    )

    category_options = selectbox_div.find_elements(By.CLASS_NAME, 'option')
    categories = []
    category_urls = []

    for option in category_options:
        category_name = option.find_element(By.CLASS_NAME, 'planShopTxt').text
        categories.append(category_name)

        driver.execute_script("arguments[0].scrollIntoView(true);", option)
        WebDriverWait(driver, 1).until(EC.element_to_be_clickable(option))
        option.click()

        time.sleep(1)
        category_urls.append(driver.current_url)

        driver.execute_script("arguments[0].scrollIntoView(true);", selectbox_button)
        driver.execute_script("arguments[0].click();", selectbox_button)

        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.selectbox-wrap[style='display: block;']"))
        )

    return categories, category_urls


# main 함수
def process_event(event):
    event_url = f"https://m.sivillage.com/shop/initPlanShop.siv?disp_ctg_no={event['id']}"
    driver.get(event_url)
    time.sleep(1)  # 페이지 로드 대기

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # HTML 배너 이미지 추출 (너비 600px 이상, 높이 400px 이상)
    valid_images = []
    banner_divs = soup.find_all('div', class_='event-detail__html-banner')
    for banner in banner_divs:
        img_tag = banner.find('img')
        if img_tag and is_valid_image(img_tag['src']):
            valid_images.append(img_tag['src'])

    # 쿠폰 정보 추출
    coupon = get_coupon_info(soup)

    # 카테고리 정보 추출 및 클릭 처리
    categories = []
    category_links = []

    try:
        # Tab형 카테고리 처리
        categories, category_links = click_tab_category()
    except Exception as e:
        print(f"Error in click_tab_category: {e}")
        # 오류 발생 시 Selectbox형 카테고리로 대체 시도
        try:
            categories, category_links = click_selectbox_category()
        except Exception as e:
            print(f"Error in click_selectbox_category: {e}")
            # 카테고리 정보 추출 실패 시 카테고리와 상품 정보 생략
            categories = []
            category_links = []

    # 각 카테고리별 상품 정보 수집 (최대 15개씩)
    category_dtos = []
    for idx, category_link in enumerate(category_links):
        category_name = categories[idx]
        category_products = get_category_products(category_link)
        category_dtos.append({
            'categoryName': category_name,
            'products': category_products
        })

    # 결과 저장
    event['promotion_images'] = valid_images
    event['coupon'] = coupon
    event['category_products'] = category_dtos


# brandEvent 유형의 각 이벤트에 대해 정보 추출
for event in brand_events:
    process_event(event)

# 결과를 파일로 저장
with open('data/brandEvent/forme/brand_events_with_details_10.json', 'w', encoding='utf-8') as f:
    json.dump(brand_events, f, ensure_ascii=False, indent=4)

# 드라이버 종료
driver.quit()