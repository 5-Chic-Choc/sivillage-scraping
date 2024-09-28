# SiVillage 데이터 스크래핑
- SIVILLAGE 리빌딩 프로젝트에 필요한 데이터를 스크래핑하는 `.py` 파일을 공유합니다.
- repository에 데이터는 업로드 하지 않습니다.
- contributor: 홍정현(상품,브랜드), 주성광(이벤트,카테고리)

<details>
  <summary> <h3>product & brand</h3> </summary>

**author : 홍정현**

브랜드, 상품 정보를 스크래핑하여 `json` 및 `csv` 파일로 저장합니다.

## 설명

### 브라우저 자동화를 사용하지 않음
- `selenium`과 같은 브라우저 자동화의 경우 `Client Side Rendering`페이지를 다룰 수 있다는 장점이 있지만, 브라우저를 직접 구동하기 때문에 시간이 매우 오래 걸립니다.
- `Server Side Rendering` 페이지의 경우 `GET` 요청을 통해 완성된 페이지를 가져옵니다. 이 경우 브라우저 자동화는 불필요하며, `GET` 요청은 브라우저 구동이 없어 성능을 개선할 수 있습니다.
- 데이터의 경우 데스크탑 페이지나 모바일 페이지나 동일하기 떄문에 모바일 페이지와 데스크탑 페이지 중 `SSR` 처리가 된 페이지를 적절히 요청하여 성능을 개선하였습니다.

### `aiohttp`, `asyncio`를 통한 비동기 요청
- 동시에 여러 개의 요청을 보낼 수 있도록하여 성능을 개선합니다.
- 초당 요청 횟수를 제한하여, 트래픽이 차단되지 않도록합니다.

### 멀티 스레딩
- 파일을 읽고 쓰는 작업은 IO intensive한 작업입니다.
- IO intensive한 파일 읽기 및 저장에 멀티 스레딩을 사용하여 성능을 개선합니다.

### 멀티 프로세싱
- 파일을 파싱하는 작업은 CPU intensive한 작업입니다.
- CPU intensive한 파일 파싱 작업을 위해 멀티 프로세싱을 사용하여 성능을 개선합니다.


## `.py` 파일 소개

### `category.py`

- 카테고리 정보를 스크래핑하여 저장합니다.

### `brand.py`

- 브랜드 정보를 스크래핑하여 저장합니다.

### `dataclass.py`

- 상품 관련 `dataclass`를 정의합니다.

### `fetch.py`

- 비동기 요청을 위한 보일러플레이트 함수

### `product_code.py`

- 카테고리 코드를 불러와, 카테고리 별 상품코드을 최대 2페이지 (최대 120개)까지 스크래핑하여 저장합니다.

### `product_detail.py`

- 상품코드를 읽어와 코드에 해당하는 상품 상세 페이지를 html 문서로 저장합니다.

### `product_data.py`

- 상품 상제 html 문서를 읽어와 상품 관련 정보를 스크래핑히야 저장합니다.

### `merge_product data`


</details>

<details>
  <summary><h3>event</h3></summary>

  **작성자 : 주성광**


- event 폴더
  - .py 및 eventlist.json
  - data 폴더 : 수집한 데이터 저장

### .py files 소개
1. `eventlist.py`
  - 이벤트 페이지에 접근해 현재 진행중인 이벤트를 수집 후 `eventlist.json`로 저장합니다.
  - 예시
    ```json
        {
        "id": "2408144542",
        "type": "brandEvent",
        "img_src": "https://image.sivillage.com/upload/C00001/s3/dspl/banner/1010/332/00/240900000506332_20240904161905.jpg?RS=350&SP=1",
        "brand": "BALMUDA",
        "title": "8주년 가전 빅 세일!",
        "description": "발뮤다, 삼성전자 최대 50% & 쿠폰 & 페이백",
        "tags": [
            "특가",
            "쿠폰",
            "페이백"
        ]
    },
    {
        "id": "E240810358",
        "type": "affiliation",
        "img_src": "https://image.sivillage.com/upload/C00001/s3/dspl/banner/2010/881/00/240800000500881_20240822150141.jpg?RS=350&SP=1",
        "brand": "이벤트",
        "title": "현대카드 x Vpay 즉시할인(9/9~9/15)",
        "description": "20만원 이상 결제 시 최대 2만원 즉시 할인",
        "tags": []
    },
    ```
      이 list를 사용해 Event의 type별로 아래 .py 파일들에서 데이터를 수집합니다.
    
2. `mallEvent.py` : 이벤트 혜택 데이터 수집
3. `brandEventVer2.py` : 브랜드 기획전 데이터 수집
-   `brandEventVer2_NoProductInfo` : 상품 데이터 정규화를 가정, 최소한의 상품데이터만 수집
5. `affiliationEvent.py` : 제휴 혜택 데이터 수집

   
각각의 파일에서 수집하는 데이터의 예시는 data 폴더를 참고하시면 됩니다.
  
- 이벤트의 90% 가량을 차지하는 `brandEvent.py`에서 추출하는 데이터 예시 (상품 데이터 간소화 버전)

```json
[
    {
        "id": "2407141475",
        "type": "brandEvent",
        "thumbnail_img": "https://image.sivillage.com/upload/C00001/s3/dspl/banner/1010/812/00/240900000508812_20240911094353.jpg?RS=350&SP=1",
        "brand": "BLOODLINE GOLF",
        "title": "최고의 장비로 퍼펙트한 라운딩",
        "description": "블러드라인 최대 60% OFF + 10% 상품쿠폰 증정",
        "tags": [
            "할인",
            "특가",
            "쿠폰"
        ],
        "promotion_images": [ //세부 이미지
            "https://image.sivillage.com/upload/C00001/fckeditor/banner/202409/1725952214757.jpg",
            "https://image.sivillage.com/upload/C00001/fckeditor/banner/202409/1725952237496.jpg"
        ],
        "coupon": {
            "name": "[블러드라인] 기간한정 10% 상품쿠폰",
            "discount": "10%",
            "period": "2024-09-16 ~ 2024-09-22",
            "kind": "상품쿠폰"
        },
        "category_products": [
            {
                "categoryName": "SPECIAL OFFER ~50%",
                "products": [
                    {
                        "goods_no": "2309891321",
                        "name": "VALE VANTA BLACK (베일 반타 블랙)"
                    },
                    {다른 상품들 ...}
                ]
            { 다른 카테고리 }: [
            ]
        }
    }
    {다른 이벤트...}
]

```

### 기타
- 이벤트 종류별로 요소가 각양 각색이고, 적절치 않은 이미지도 많아 이미지의 크기가 일정 px 이상인 데이터만 수집하도록 했습니다.
- 긍정적인 수정 사항, 수집 데이터, 정제/가공 데이터 등 PR 또는 공유해주시면 감사하겠습니다.
  
</details>
<details>
  <summary><h3>category</h3></summary>

**작성자 : 주성광**

- category.md
```
## 뷰티
- 향수
    - 오 드 뚜왈렛
    - 오 드 퍼퓸
    - 코롱
    - 기타 향수
    - 헤어 퍼퓸
- 스킨케어
    - 스킨/토너/미스트
        - 토너
        - 토너 패드
        - 미스트
```

- categoryStructure.json
```
[
    {
        "name": "뷰티",
        "children": [
            {
                "name": "향수",
                "children": [
                    {
                        "name": "오 드 뚜왈렛",
                        "children": []
```

- category.csv
<img width="752" alt="image" src="https://github.com/user-attachments/assets/23b7efcd-aea6-49ef-b59f-441ea1aefd9e">


</details>



