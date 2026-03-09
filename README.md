# 📊 KR Market Pulse

> 한국은행 ECOS Open API 기반 거시경제 & 투자 시그널 대시보드

**Live URL**: `https://{your-username}.github.io/kr-market-pulse`

---

## 🚀 5분 셋업

### 1. Repository 생성 & Push
```bash
git init
git add .
git commit -m "🚀 Initial commit: KR Market Pulse"
git remote add origin https://github.com/{your-username}/kr-market-pulse.git
git push -u origin main
```

### 2. ECOS API 키 등록
```
GitHub repo → Settings → Secrets and variables → Actions
→ New repository secret
  Name:  ECOS_API_KEY
  Value: [한국은행 ECOS Open API 인증키]
```

### 3. GitHub Pages 활성화
```
Settings → Pages → Source: Deploy from a branch → Branch: main / (root)
```

### 4. 첫 데이터 수동 실행
```
Actions → 📊 KR Market Pulse - Daily Data Fetch → Run workflow
```

이후 **매일 오전 7시 KST** 자동 갱신됩니다.

---

## 📂 프로젝트 구조

```
kr-market-pulse/
├── .github/
│   └── workflows/
│       └── fetch-data.yml      ← 매일 자동 데이터 갱신
├── data/                        ← ECOS API 결과 JSON 캐시
│   ├── biz_analysis.json       ← 기업경영분석 (ROE, OPM 등)
│   ├── rates.json              ← 기준금리, 국고채
│   ├── money.json              ← M1, M2 통화량
│   ├── forex.json              ← 환율 (USD, JPY, EUR)
│   ├── flow_of_funds.json      ← 자금순환
│   ├── bop.json                ← 국제수지
│   ├── trade.json              ← 수출입
│   └── macro.json              ← GDP, CPI, PPI, 소비자심리
├── scripts/
│   └── fetch_ecos.py           ← ECOS 데이터 수집 스크립트
├── index.html                  ← 메인 대시보드 (단일 파일)
└── README.md
```

---

## 📊 탭 구성

| 탭 | 주요 내용 |
|----|----------|
| **Overview** | 12개 핵심 KPI + 금리·기업수익성·물가·경상수지·GDP 차트 |
| **기업수익성** | 제조업 OPM/ROE/ROA, 대기업 vs 중소기업, 이자보상배율 |
| **자금순환** | Sankey 자금 흐름, 가계 자산구성, 기업 자금조달 |
| **대외자금흐름** | 경상수지 분해, 환율, 수출입, 품목·지역별 구조 |
| **투자 시그널** | 4대 카테고리 100점 스코어링, 금리역전·실질금리·유동성·이익 모멘텀 |

---

## 📡 ECOS API 데이터 목록

| 카테고리 | 지표 | 통계 코드 |
|---------|------|----------|
| **기업수익성** | 영업이익률, ROE, ROA, 부채비율 | 502Y002, 502Y003 |
| **금리** | 기준금리, 국고채 3Y/10Y, CD, 회사채 | 722Y001, 817Y002 |
| **통화** | M1, M2 (계절조정) | 101Y004 |
| **환율** | USD/KRW, JPY/KRW, EUR/KRW | 731Y001 |
| **자금순환** | 부문별 자금운용 | 221Y011 |
| **국제수지** | 경상·상품·서비스수지 | 901Y032 |
| **수출입** | 수출, 수입 (통관기준) | 403Y003 |
| **거시** | 실질GDP, CPI, PPI, 소비자심리지수 | 다수 |

---

## ⚙️ 투자 시그널 스코어링 기준

```
총점 100점 = 금리·통화정책(25) + 유동성·통화량(25) + 기업이익(25) + 대외수지(25)

70점 이상  → ▲ 매수 우호
55~70점    → ↗ 다소 우호
40~55점    → → 중립
25~40점    → ↘ 다소 비우호
25점 미만  → ▼ 매수 비우호
```

---

## 📝 라이선스
MIT License | 데이터 출처: 한국은행 경제통계시스템(ECOS) | © 2026
