# PROJECT: We&Olufsen
## 소개
- [Bango & Olufsen](https://www.bang-olufsen.com/ko/kr) 클론 사이트
- 고급 스피커 판매 사이트: 카테고리 분류, 회원관리, 장바구니, 주문, 정렬기능, 페이지네이션

## 팀 인원
- BE(2명): 손찬규, 박서윤
- FE(4명): 신수정, 심동규, 이현주, 정훈조

## 개발 기간
- 개발 기간 : 2022-07-18 ~ 2022-07-29 (12일)
- 협업 툴 : Slack, Trello, Github, Notion

## 기술 스택
|                                                Language                                                |                                                Framwork                                                |                                               Database                                               |                                                     ENV                                                      |                                                   HTTP                                                   |                                                  Deploy                                                 |
| :----------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------: |:------------------------------------------------------------------------------------------------------: |
| <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> | <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> | <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=black"> | <img src="https://img.shields.io/badge/miniconda3-44A833?style=for-the-badge&logo=anaconda&logoColor=white"> | <img src="https://img.shields.io/badge/postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white"> | <img src="https://img.shields.io/badge/aws-232F3E?style=for-the-badge&logo=Amazon AWS&logoColor=white"> 


## Backend 역할
**박서윤**
- 회원가입(SignUpView)
  - POST
  - 정규식 통해 이메일과 패스워드 조건 확인
  - email unique 처리
  - 패스워드 암호화
- 상품상세페이지(ProductDetailView)
  - GET
  - 해당 product_id의 상세페이지 구현
- 주문페이지(OrderView)
  - POST
  - transaction.atomic()으로 order에서 발생할 오류 방지
- 장바구니(CartView)
  - POST, GET, DELETE, PATCH
  - get_or_create 이용하여 장바구니에 존재여부 고려

**손찬규**
- 로그인(LoginView)
  - POST
  - JWT를 이용하여 토큰 발급
- 상품페이지(ProductListView)
  - GET
  - limit, offset을 통한 pagination 구현
  - Q객체 사용: 데이터 정렬 후, 전송


## 모델링
<img width="1400px" src="https://user-images.githubusercontent.com/91110192/181713064-a61209dc-5678-491c-b41e-5d59c664fb56.png"/>

## 사이트 시현 영상
<img src="https://user-images.githubusercontent.com/91110192/181877555-7427a226-8772-4f29-a386-0796c8839418.gif" width="1000px">

## API 명세서
[WeOlufsen API](https://pastoral-slice-3c4.notion.site/API-40dd9ab8a58f442baad377974f308ecc)
