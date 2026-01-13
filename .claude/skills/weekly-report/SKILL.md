---
name: weekly-report
description: 비블레시아 주간 분석 보고서 생성. Amplitude 데이터를 수집하고 인사이트가 포함된 HTML 보고서를 자동 생성합니다.
allowed-tools: Bash, Write, Edit, mcp__Amplitude__query_charts
user-invocable: true
---

# 비블레시아 주간 보고서 생성

"분석 보고서를 작성해줘" 또는 `/weekly-report` 명령으로 실행됩니다.

Amplitude에서 데이터를 수집하고, "비블레시아 X월 X주차 보고서" 형식의 HTML 보고서를 생성합니다.

## 차트 정보

| 메트릭 | Chart ID |
|--------|----------|
| WAU (Weekly Active Users) | kjwedsn |
| NAU (Weekly New Users) | cj3mctf |
| Weekly Retention | 40q1uy5i |
| Weekly Retention Over Time | l0v3zbcc |

## 실행 단계

### Step 1: Amplitude 데이터 조회

`mcp__Amplitude__query_charts` 도구를 사용하여 차트 데이터를 조회합니다.

첫 번째 호출:
```
chartIds: ["kjwedsn", "cj3mctf", "40q1uy5i"]
```

두 번째 호출:
```
chartIds: ["l0v3zbcc"]
```

### Step 2: 데이터 파싱 및 Excel 스크립트 업데이트

조회된 CSV 데이터를 파싱하여 `generate_amplitude_report.py`의 데이터를 업데이트합니다.

**CSV 응답 구조:**
- WAU/NAU: 날짜별 값 배열
- Retention: 코호트별 테이블 형태

`generate_amplitude_report.py` 파일의 `WAU_DATA`, `NAU_DATA`, `RETENTION_DATA`를 업데이트합니다.

### Step 3: Excel 파일 생성

```bash
cd /Users/yuhwan/Desktop/Development/biblessia-analysis
source venv/bin/activate
python generate_amplitude_report.py
```

### Step 4: HTML 보고서 생성

```bash
python scripts/generate_html_report.py -j
```

`-j` 옵션으로 JSON 데이터를 확인합니다.

**참고:** 이번 주 데이터는 아직 수집 중이므로 자동으로 제외됩니다.
보고서 타이틀은 자동으로 "비블레시아 X월 X주차 보고서" 형식으로 생성됩니다.

### Step 5: 데이터 분석 및 인사이트 작성

JSON 데이터를 분석하여 다음 인사이트를 작성합니다:

#### Summary Insight
- 전체 핵심 지표 요약
- 가장 주목할 만한 변화
- 권장 액션 아이템

#### WAU Insight
- 전체 기간 성장률 계산
- 트렌드 패턴 (상승/하락/정체)
- 이상치 또는 급변 구간 식별
- 피크 시점과 원인 추정

#### NAU Insight
- 신규 사용자 유입 패턴
- WAU 대비 NAU 비율 분석
- 마케팅/시즌 효과 추정

#### Retention Insight
- Week 1 리텐션 평가 (업계 평균: 40-60%)
- 리텐션 드롭 구간 식별
- 코호트별 비교 분석

#### Retention Over Time Insight
- 시간에 따른 리텐션 변화 추이
- 최근 코호트 vs 과거 코호트 비교
- 개선/악화 트렌드

### Step 6: HTML 리포트 생성

인사이트를 포함하여 최종 HTML을 생성합니다.

```bash
python scripts/generate_html_report.py
```

### Step 7: 인사이트 삽입

생성된 HTML 파일에서 다음 placeholder를 인사이트로 교체합니다:

- `<!-- SUMMARY_INSIGHT -->` → Summary 인사이트
- `<!-- WAU_INSIGHT -->` → WAU 분석
- `<!-- NAU_INSIGHT -->` → NAU 분석
- `<!-- RETENTION_INSIGHT -->` → 리텐션 분석
- `<!-- RETENTION_OVER_TIME_INSIGHT -->` → 리텐션 추이 분석

Edit 도구를 사용하여 각 placeholder를 교체합니다.

### Step 8: docs 폴더에 배포

보고서를 GitHub Pages용 docs 폴더에 복사합니다:

```bash
# index.html 업데이트
cp reports/analysis_report_YYYY-MM-DD.html docs/index.html

# archive에도 저장
cp reports/analysis_report_YYYY-MM-DD.html docs/archive/YYYY-MM-DD.html
```

### Step 9: Git Push

변경사항을 커밋하고 푸시합니다:

```bash
git add docs/
git commit -m "Update weekly report: YYYY-MM-DD"
git push
```

### Step 10: 완료

사용자에게 다음 정보를 제공합니다:

1. **로컬 파일:** `reports/analysis_report_YYYY-MM-DD.html`
2. **GitHub Pages URL:** `https://biblessia.github.io/biblessia-analysis/archive/YYYY-MM-DD.html`

GitHub Pages 배포는 push 후 1-2분 정도 소요됩니다.

## 인사이트 작성 가이드

### 분석 시 고려사항

**WAU/NAU:**
- 주간 변화율: `(현재 - 이전) / 이전 * 100`
- 4주 이동평균으로 트렌드 파악
- 급변(±30% 이상) 구간에 주목

**리텐션:**
- Week 1: 40-60%가 양호, 60% 이상 우수
- Week 4: 30% 이상 유지가 목표
- Week 8+: 20% 이상이면 핵심 사용자층 형성

### 인사이트 작성 톤
- 데이터 기반의 객관적 분석
- 숫자와 %를 구체적으로 명시
- 가능한 원인/가설 제시
- 실행 가능한 권장사항 포함

## 파일 구조

```
reports/
├── amplitude_report_YYYY-MM-DD.xlsx  (중간 산출물)
└── analysis_report_YYYY-MM-DD.html   (최종 보고서)
```
