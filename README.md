# 키움 API 자동매매 시스템

키움증권 RestAPI를 활용한 실시간 조건검색 기반 자동매매 시스템

---

## 🎯 프로젝트 목표

조건검색식에 편입된 종목을 실시간으로 감지하여 자동으로 매수 주문을 실행하는 시스템 구축

---

## 📁 프로젝트 구조

```
AST/
├── main.py                 # 메인 실행 파일
├── issue_token.py          # 토큰 발급 스크립트
├── config.py               # 설정 관리 (실전/모의투자 분리)
├── requirements.txt        # 필수 라이브러리 목록
├── .env.example           # 환경 변수 템플릿
├── .gitignore            # Git 제외 파일 설정
│
├── auth/                  # 인증 모듈
│   ├── __init__.py
│   └── token_manager.py   # 토큰 발급/관리 (au10001, au10002) ✅
│
├── trading/               # 매매 모듈
│   ├── __init__.py
│   ├── order.py           # 주문 실행 (kt10000, kt10001)
│   └── account.py         # 계좌 조회 (ka10075, ka01690)
│
├── search/                # 조건검색 모듈
│   ├── __init__.py
│   ├── condition.py       # 조건검색 관리 (ka10171, ka10172)
│   └── realtime.py        # 실시간 감지 (ka10173, ka10174)
│
├── utils/                 # 유틸리티
│   ├── __init__.py
│   ├── logger.py          # 로깅 ✅
│   └── api_client.py      # API 클라이언트 베이스 ✅
│
├── logs/                  # 로그 파일 저장
│
└── API_GUIDE/             # 키움 API 문서 (25/187개)
    ├── API_LIST.md
    ├── au10001.md         # 접근토큰 발급
    ├── au10002.md         # 접근토큰 폐기
    ├── ka10171-174.md     # 조건검색 API
    └── kt10000-003.md     # 주문 API
```

---

## ⚙️ 환경 설정

### 1. 라이브러리 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
```bash
cp .env.example .env
```

`.env` 파일에 실제 API 키 입력:
- `MODE`: `real` (실전투자) 또는 `virtual` (모의투자)
- `REAL_APPKEY`, `REAL_SECRETKEY`: 실전투자 인증 정보
- `VIRTUAL_APPKEY`, `VIRTUAL_SECRETKEY`: 모의투자 인증 정보
- `ACCOUNT_NO`: 계좌번호

### 3. 설정 확인
```bash
python config.py
```

### 4. 토큰 발급
```bash
python issue_token.py
```

토큰 발급 스크립트는 다음 작업을 수행합니다:
- 설정된 APPKEY와 SECRETKEY로 접근 토큰 발급
- .env 파일에 토큰 자동 저장 (선택)
- 토큰 만료 일시 확인

---

## 🚀 실행 방법

### 토큰 발급만 하기
```bash
python issue_token.py
```

### 자동매매 시스템 실행
```bash
python main.py
```

**현재 구현 상태:**
- ✅ 토큰 자동 발급/갱신
- ✅ 토큰 유효성 확인
- ⏳ 실시간 조건검색 (예정)
- ⏳ 자동매매 (예정)

---

## 🔧 개발 시 주의사항

### 필드 매핑 주의
- `secretkey` (not `appsecret`)
- `token` (not `access_token`)

### 실전/모의투자 구분
- **모의투자**: `MODE=virtual` (기본값, 안전)
- **실전투자**: `MODE=real` (주의 필요!)

---

## 📚 참고 문서
- [키움 API 포털](https://openapi.kiwoom.com/guide/apiguide/)

---
