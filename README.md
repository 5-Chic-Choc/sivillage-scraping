# SiVillage 데이터 스크래핑
- 데이터는 포함하지 않습니다.
- assignee: 주성광(이벤트,카테고리)

<details>
  <summary><h2>event</h2></summary>

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
  <summary><h2>category</h2></summary>

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



