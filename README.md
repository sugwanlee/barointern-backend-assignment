# 바로인턴 백엔드 과제
 - 배포 주소: http://3.38.135.6:8000

## 개요
바로인턴 백엔드 개발자 인턴 선발을 위한 과제로, 사용자 인증 시스템을 구현한 RESTful API 서버입니다. JWT 기반 인증, 회원가입/로그인 API, 그리고 테스트 및 문서화를 포함합니다.

## 구현 기능

### 1. 사용자 인증 시스템
- 회원가입 API: 사용자 정보를 입력받아 계정 생성
- 로그인 API: 사용자 인증 및 JWT 토큰 발급
- 인증 테스트 API: 토큰 유효성 검증용 엔드포인트
- 비밀번호 유효성 검사 규칙 수정: 공통 비밀번호 및 숫자만으로 구성된 비밀번호 제한 해제 (최소 8자 길이만 유지)

### 2. JWT 인증
- Simple JWT 라이브러리를 활용한 토큰 기반 인증 구현
- 액세스 토큰 발급 및 검증
- 토큰 만료 시간 설정 및 관리

### 3. 테스트 코드
- 각 API 엔드포인트 동작 검증을 위한 테스트 코드 작성
- 성공/실패 케이스 모두 테스트하여 견고성 확보

### 4. API 문서화
- Swagger(drf-spectacular)를 활용한 API 문서 자동화
- 각 API의 요청/응답 구조 및 예시 제공
- `/swagger` 경로에서 문서 확인 가능

### 5. AWS EC2 배포
- AWS EC2 인스턴스에 배포 완료
- Gunicorn을 사용하여 백그라운드에서 안정적으로 실행
- 접속 정보: `http://3.38.135.6:8000` --> 과제 요구사항 대로 0.0.0.0:8000으로 배포
- API 문서: `http://3.38.135.6:8000/swagger` 

## 기술 스택
- **언어 및 프레임워크**: Python 3.11, Django 5.2, Django REST Framework 3.16.0
- **인증**: Simple JWT
- **문서화**: drf-spectacular (Swagger/OpenAPI)
- **데이터베이스**: SQLite
- **테스트**: Django Test Framework
- **배포**: AWS EC2, Gunicorn

## 폴더 구조
```
/
├── assignment/       # 메인 프로젝트 폴더
│   ├── accounts/     # 사용자 인증 관련 앱
│   │   ├── views.py          # API 뷰 정의
│   │   ├── serializers.py    # 데이터 직렬화/역직렬화
│   │   ├── urls.py           # URL 라우팅
│   │   ├── schemas.py        # API 문서화 스키마
│   │   ├── tests/            # 테스트 코드 디렉토리
│   │   ├── models.py         # 데이터 모델
│   │   ├── exception_handler.py # 예외 처리
│   │   ├── migrations/       # 데이터베이스 마이그레이션
│   │   ├── apps.py           # 앱 설정
│   │   └── admin.py          # 관리자 설정
│   ├── config/        # 프로젝트 설정
│   │   ├── settings.py       # 프로젝트 설정
│   │   ├── urls.py           # 메인 URL 라우팅
│   │   ├── asgi.py           # ASGI 설정
│   │   └── wsgi.py           # WSGI 설정
│   ├── manage.py      # Django 관리 스크립트
│   └── db.sqlite3     # SQLite 데이터베이스
├── venv/             # 가상환경 (생성 후)
├── requirements.txt  # 의존성 패키지 목록
├── .env              # 환경변수 설정 파일
└── .gitignore        # Git 무시 파일 목록
```

## 실행 방법

### 1-1. 환경 설정
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```
### 1-2 환경 변수 설정
```bash
# .env 파일 생성
touch .env

# .env 파일 편집
nano .env

# 환경 변수 설정
SECRET_KEY=your_secret_key
```

### 2. 서버 실행
```bash
# 데이터베이스 마이그레이션
python manage.py migrate

# 개발 서버 실행
python manage.py runserver
```

### 3. API 테스트
- 회원가입: POST `/signup/`
- 로그인: POST `/login/`
- 인증 테스트: POST `/auth-test/`

### 회원가입 API
- URL: `/signup/`
- Method: POST
- Request Body:
  ```json
  {
    "username": "JIN HO2",
    "password": "12341232",
    "nickname": "Mentos"
  }
  ```
- Response: 201 Created

### 로그인 API
- URL: `/login/`
- Method: POST
- Request Body:
  ```json
  {
    "username": "JIN HO2",
    "password": "12341232",
  }
  ```
- Response: 200 OK (JWT 토큰 포함)

### 인증 테스트 API
- URL: `/auth-test/`
- Method: POST
- Headers: `Authorization: Bearer {token}`
- Response: 200 OK (인증 성공 메시지)

