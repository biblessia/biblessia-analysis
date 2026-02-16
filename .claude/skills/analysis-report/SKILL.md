# Amplitude Analysis Report Generator

reports 폴더의 최신 Excel 파일을 분석하여 인사이트가 포함된 HTML 리포트를 생성합니다.

## 실행 단계

### Step 1: 데이터 추출 및 기본 HTML 생성

```bash
cd /Users/yuhwan/Desktop/Development/biblessia-analysis
source venv/bin/activate
python scripts/generate_html_report.py -j
```

`-j` 옵션으로 JSON 데이터를 확인합니다.

**참고:** 이번 주 데이터는 아직 수집 중이므로 자동으로 제외됩니다.

### Step 1.5: 이전 보고서 읽기 (MoM 비교용)

`docs/archive/` 디렉토리에서 가장 최근의 이전 보고서를 찾아 Read 도구로 읽습니다.

**절차:**
1. `docs/archive/` 내 HTML 파일 목록을 확인합니다 (패턴: `YYYY-MM-DD.html`)
2. 오늘 날짜를 제외하고 가장 최근 날짜의 보고서를 선택합니다
3. 해당 HTML 파일을 Read 도구로 읽습니다
4. 다음 핵심 지표를 추출합니다:
   - 최신 WAU 값 및 WoW 변화율
   - 최신 NAU 값 및 WoW 변화율
   - Week 1 리텐션 평균 및 최근 코호트 리텐션
   - 당시 인사이트 내용 (트렌드 판단 및 권장사항)

**이전 보고서가 없는 경우:** MoM 비교를 건너뛰고 현재 데이터만으로 인사이트를 작성합니다.

### Step 2: 데이터 분석 및 인사이트 작성

JSON 데이터를 분석하고, Step 1.5에서 추출한 이전 보고서 지표와 비교하여 다음 인사이트를 작성합니다:

#### Summary Insight
- 전체 핵심 지표 요약
- 가장 주목할 만한 변화
- 권장 액션 아이템
- **[MoM]** 전월 보고서에서 제시한 권장사항의 후속 평가 (실행 여부, 효과)

#### WAU Insight
- 전체 기간 성장률 계산
- 트렌드 패턴 (상승/하락/정체)
- 이상치 또는 급변 구간 식별
- 피크 시점과 원인 추정
- **[MoM]** 전월 보고서 대비 WAU 변화 (절대값 및 %)

#### NAU Insight
- 신규 사용자 유입 패턴
- WAU 대비 NAU 비율 분석
- 마케팅/시즌 효과 추정
- **[MoM]** 전월 대비 NAU 트렌드 변화 (유입 증가/감소 추세)

#### Retention Insight
- Week 1 리텐션 평가 (업계 평균: 40-60%)
- 리텐션 드롭 구간 식별
- 코호트별 비교 분석
- **[MoM]** 전월 대비 리텐션 개선/악화 평가

#### Retention Over Time Insight
- 시간에 따른 리텐션 변화 추이
- 최근 코호트 vs 과거 코호트 비교
- 개선/악화 트렌드
- **[MoM]** 전월 보고서 시점과 비교한 장기 리텐션 추이 변화

### Step 3: HTML 리포트 생성

인사이트를 포함하여 최종 HTML을 생성합니다.

```bash
python scripts/generate_html_report.py
```

### Step 4: 인사이트 삽입

생성된 HTML 파일에서 다음 placeholder를 인사이트로 교체합니다:

- `<!-- SUMMARY_INSIGHT -->` → Summary 인사이트
- `<!-- WAU_INSIGHT -->` → WAU 분석
- `<!-- NAU_INSIGHT -->` → NAU 분석
- `<!-- RETENTION_INSIGHT -->` → 리텐션 분석
- `<!-- RETENTION_OVER_TIME_INSIGHT -->` → 리텐션 추이 분석

Edit 도구를 사용하여 각 placeholder를 교체합니다.

### Step 5: 완료

리포트 파일 경로를 사용자에게 알립니다:
- 위치: `reports/analysis_report_YYYY-MM-DD.html`
- 브라우저에서 열어 확인: `open reports/analysis_report_*.html`

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

### 예시 인사이트

```
WAU가 지난 6개월간 185명에서 1,194명으로 545% 성장했습니다.

주요 관찰:
- 11월 초 급성장: 545명 → 1,100명 (+102%), 마케팅 캠페인 효과 추정
- 12월 말 피크: 2,003명, 연말/신년 효과
- 1월 둘째주 조정: 2,061명 → 1,194명 (-42%), 연휴 효과 소멸로 정상화 과정

권장사항:
- 11월 마케팅 캠페인의 성공 요인 분석 및 재현
- 연말 피크 사용자의 리텐션 집중 관리
```

## 파일 구조

```
reports/
├── amplitude_report_YYYY-MM-DD.xlsx  (입력)
└── analysis_report_YYYY-MM-DD.html   (출력)
```
