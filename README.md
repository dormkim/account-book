# 가계부 내역 조회 서비스

가계부를 작성하고 수정 / 삭제를 통하여 내역을 관리할 수 있는 서비스

## 패키지 관리 툴
- poetry

### 소스코드 관리 툴
- isort
- black
- flake8
  
### 서비스 실행
```
$ docker-compose build .
$ docker-compose up
```

### API 명세 확인
- 유저 인증 및 관리
  - email / password / nickname(Optional)를 통해 가입
  - 이메일 중복 가입은 불가능
  - bcrypt 방식으로 password 를 암호화
  - 가입에 성공하여 로그인 하게 되면 jwt token 을 발급(6시간 유효)
  - token 없이 가계부 내역을 조회할 수 없음
- 가계부 내역 관리
  - amount / memo(Optional) / is_withdrawn(출금여부)를 입력 후 생성
  - 본인이 작성한 가계부 전체 내역 확인 가능
  - 특정 가계부 내역 삭제가능
  - 삭제되지 않은 특정 가계부 내역의 세부내역 조회가능
  - 삭제되지 않은 특정 가계부 내역의 세부내역 수정가능
- 자세한 API 명세는 아래 링크에서 확인가능
  - 127.0.0.1:8000/docs

