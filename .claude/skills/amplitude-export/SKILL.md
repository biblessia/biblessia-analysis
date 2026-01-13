---
name: amplitude-export
description: Amplitude 데이터를 Excel로 내보내기. Export Amplitude WAU, NAU, Retention data to Excel file.
allowed-tools: Bash, Write
---

# Amplitude Data Export to Excel

Amplitude에서 주요 메트릭 데이터를 가져와 Excel 파일로 저장합니다.

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

```
chartIds: ["kjwedsn", "cj3mctf", "40q1uy5i"]
```

그리고 추가로:
```
chartIds: ["l0v3zbcc"]
```

### Step 2: 데이터 파싱 및 Python 스크립트 생성

조회된 CSV 데이터를 파싱하여 Python 스크립트를 생성합니다.

**CSV 응답 구조:**
- WAU/NAU: `["Segment", "날짜1", "날짜2", ...]`, `["South Korea", 값1, 값2, ...]`
- Retention: 코호트별 테이블 형태

### Step 3: Excel 파일 생성

venv를 사용하여 Python 스크립트를 실행합니다.

```bash
cd /Users/yuhwan/Desktop/Development/biblessia-analysis
source venv/bin/activate
python generate_amplitude_report.py
```

venv가 없으면 먼저 생성:
```bash
python3 -m venv venv
source venv/bin/activate
pip install openpyxl
```

### Step 4: Python 스크립트 템플릿

`generate_amplitude_report.py` 파일을 생성하고 아래 구조를 사용합니다:

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime

# 데이터 정의 (Amplitude에서 가져온 데이터로 교체)
WAU_DATA = {
    "dates": [...],  # Amplitude에서 가져온 날짜 배열
    "values": [...]  # Amplitude에서 가져온 값 배열
}

NAU_DATA = {
    "dates": [...],
    "values": [...]
}

RETENTION_DATA = [...]  # Retention 테이블 데이터

# 스타일 정의
HEADER_FILL = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
HEADER_FONT = Font(bold=True, color="FFFFFF")
BORDER = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

def create_workbook():
    wb = Workbook()
    # Summary, WAU, NAU, Weekly Retention 시트 생성
    # ... (세부 구현)
    return wb

def main():
    wb = create_workbook()
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f'amplitude_report_{today}.xlsx'
    wb.save(filename)
    print(f"Excel file created: {filename}")

if __name__ == "__main__":
    main()
```

## Excel 시트 구성

| 시트 | 내용 |
|------|------|
| Summary | 최신 WAU, NAU, Week 1 Retention + 이전 주 대비 변화율 |
| WAU | 주간 활성 사용자 추이 (날짜, 값) |
| NAU | 주간 신규 사용자 추이 (날짜, 값) |
| Weekly Retention | 코호트별 리텐션 테이블 |

## 완료 후

파일 경로를 사용자에게 알려줍니다:
- 파일명: `amplitude_report_YYYY-MM-DD.xlsx`
- 위치: 현재 작업 디렉토리
