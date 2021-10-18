## BBADDA 프로젝트 Front-end/Back-end 소개
- MLB 굿즈 온라인 샵 [MLB](https://www.mlb-korea.com/) 클론 프로젝트
- 짧은 프로젝트 기간동안 개발에 집중해야 하므로 디자인/기획 부분만 클론했습니다.
- 개발은 초기 세팅부터 전부 직접 구현했으며, 백앤드와 연결하여 실제 사용할 수 있는 서비스 수준으로 개발한 것입니다.
### 개발 인원 및 기간
- 개발기간 : 2021/10/5 ~ 2021/10/15
- 개발 인원 : 프론트엔드 4명, 백엔드 2명
- [프론트엔드 github 링크](https://github.com/wecode-bootcamp-korea/25-1st-bbadda-frontend)
- [백엔드 github 링크](https://github.com/wecode-bootcamp-korea/25-1st-bbadda-backend) -->
### 프로젝트 선정이유
- 이 사이트는 추가적인 학습 뿐 아니라 배운 내용들을 활용해볼 것들이 많아 선정하게 되었습니다.

## 적용 기술 및 구현 기능
### 적용 기술
> - Front-End : React.js, sass
> - Back-End : Python, Django web framework, JWT, Bcrypt, My SQL
> - Common :
### 구현 기능
> - Bcrypt를 활용한 회원정보 암호화 적용 및 JWT를 적용한 로그인 기능 구현
> - 각 메뉴에 따른 상품 리스트업(정렬 및 페이지네이션 일부 구현)
> - db에 저장된 정보를 바탕으로 데이터 통신을 통한 상품 상세데이터 출력
> - 상품 상세페이지에서 설정한 정보(상품, 사이즈, 수량)를 주문페이지로 전송하여 해당 상품을 주문할 수 있는 기능 구현
> - 주문완료 시 각 상품의 수량 차감, 유저의 포인트 차감, 판매량 증가 적용
#### Backend
> - User, Product, Order 각각의 테이블 생성
> - Query Parameter를 활용한 정렬 기능 및 페이지네이션 기능 구현
> - Q객체를 활용한 메뉴 필터링 기능 구현
> - 주문 기능에 transaction을 적용하여 특정 부분에서만 발생하는 에러 방지
## Reference
- 이 프로젝트는 [MLB](https://www.mlb-korea.com/) 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 copyright free 사이트인 https://pixabay.com/ 의 이미지들을 취합하여 제작하였습니다.
