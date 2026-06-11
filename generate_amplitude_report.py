#!/usr/bin/env python3
"""Amplitude 데이터를 Excel로 내보내기"""

import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime

# 내보내기 폴더 설정
EXPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")

# 데이터 정의 (Amplitude에서 가져온 데이터 - 2026-06-11 업데이트, 글로벌 기준 / 마지막 미완성주(06-08) 제외)
WAU_DATA = {
    "dates": ["2025-12-22","2025-12-29","2026-01-05","2026-01-12","2026-01-19","2026-01-26","2026-02-02","2026-02-09","2026-02-16","2026-02-23","2026-03-02","2026-03-09","2026-03-16","2026-03-23","2026-03-30","2026-04-06","2026-04-13","2026-04-20","2026-04-27","2026-05-04","2026-05-11","2026-05-18","2026-05-25","2026-06-01"],
    "values": [1392,2088,2135,2077,2096,2192,2344,2297,2219,2470,2803,2983,2944,2996,3043,2989,3140,3030,3033,3082,3091,3051,3071,3122]
}

# WAU 지역별 분석 (한국 vs 한국 외) - 한국: country is South Korea / 한국 외: country is not South Korea
WAU_BY_REGION_DATA = {
    "dates": ["2025-12-22","2025-12-29","2026-01-05","2026-01-12","2026-01-19","2026-01-26","2026-02-02","2026-02-09","2026-02-16","2026-02-23","2026-03-02","2026-03-09","2026-03-16","2026-03-23","2026-03-30","2026-04-06","2026-04-13","2026-04-20","2026-04-27","2026-05-04","2026-05-11","2026-05-18","2026-05-25","2026-06-01"],
    "korea": [1348,2010,2075,2002,2030,2120,2273,2224,2140,2412,2728,2922,2888,2924,2978,2924,3073,2973,2973,2987,2979,2943,2955,3008],
    "non_korea": [60,105,87,105,120,110,121,120,117,90,96,76,86,95,89,88,91,84,91,120,138,130,143,134]
}

NAU_DATA = {
    "dates": ["2025-12-22","2025-12-29","2026-01-05","2026-01-12","2026-01-19","2026-01-26","2026-02-02","2026-02-09","2026-02-16","2026-02-23","2026-03-02","2026-03-09","2026-03-16","2026-03-23","2026-03-30","2026-04-06","2026-04-13","2026-04-20","2026-04-27","2026-05-04","2026-05-11","2026-05-18","2026-05-25","2026-06-01"],
    "values": [493,757,382,272,267,341,369,250,245,377,409,508,361,315,329,359,273,236,313,248,291,224,277,279]
}

RETENTION_DATA = [
    ["Segment", "Start Date", "Users", "Week 0", "Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6", "Week 7", "Week 8", "Week 9", "Week 10", "Week 11", "Week 12", "Week 13", "Week 14", "Week 15", "Week 16"],
    ["Global", "Overall", "Retained", 5044, 2782, 2125, 1803, 1532, 1324, 1092, 975, 833, 694, 574, 495, 401, 270, 155, 69, 50],
    ["Global", "Overall", "Retained %", "100.0%", "58.38%", "47.35%", "42.28%", "38.56%", "35.54%", "32.0%", "30.7%", "28.69%", "27.28%", "25.91%", "26.05%", "26.06%", "26.19%", "24.92%", "28.16%", "20.41%"],
    ["Global", "Jun 01, 2026", 279, 279, 157],
    ["Global", "May 25, 2026", 277, 277, 178, 133],
    ["Global", "May 18, 2026", 224, 224, 131, 110, 90],
    ["Global", "May 11, 2026", 291, 291, 155, 134, 121, 101],
    ["Global", "May 04, 2026", 248, 248, 151, 114, 96, 89, 69],
    ["Global", "Apr 27, 2026", 313, 313, 209, 164, 141, 117, 117, 84],
    ["Global", "Apr 20, 2026", 236, 236, 131, 116, 96, 95, 78, 78, 57],
    ["Global", "Apr 13, 2026", 273, 273, 158, 115, 123, 108, 93, 86, 84, 69],
    ["Global", "Apr 06, 2026", 359, 359, 231, 185, 165, 152, 132, 120, 114, 116, 88],
    ["Global", "Mar 30, 2026", 329, 329, 151, 142, 114, 109, 91, 85, 94, 72, 68, 54],
    ["Global", "Mar 23, 2026", 315, 315, 165, 135, 110, 101, 84, 78, 74, 68, 68, 64, 53],
    ["Global", "Mar 16, 2026", 361, 361, 202, 160, 134, 134, 130, 107, 99, 97, 100, 88, 85, 69],
    ["Global", "Mar 09, 2026", 508, 508, 285, 238, 226, 187, 180, 163, 148, 139, 130, 133, 123, 117, 71],
    ["Global", "Mar 02, 2026", 409, 409, 258, 211, 205, 179, 174, 146, 141, 132, 128, 111, 115, 113, 101, 82],
    ["Global", "Feb 23, 2026", 377, 377, 241, 186, 167, 161, 140, 127, 129, 119, 118, 106, 99, 97, 98, 94, 68],
    ["Global", "Feb 16, 2026", 245, 245, 136, 115, 105, 100, 105, 102, 92, 90, 82, 72, 73, 74, 71, 61, 69, 50],
]

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

    # Summary 시트
    ws_summary = wb.active
    ws_summary.title = "Summary"
    create_summary_sheet(ws_summary)

    # WAU 시트
    ws_wau = wb.create_sheet("WAU")
    create_timeseries_sheet(ws_wau, "Weekly Active Users (WAU)", WAU_DATA)

    # WAU 지역별 시트 (한국 vs 한국 외)
    ws_wau_region = wb.create_sheet("WAU by Region")
    create_region_sheet(ws_wau_region, "WAU by Region (Korea vs Non-Korea)", WAU_BY_REGION_DATA)

    # NAU 시트
    ws_nau = wb.create_sheet("NAU")
    create_timeseries_sheet(ws_nau, "Weekly New Active Users (NAU)", NAU_DATA)

    # Retention 시트
    ws_retention = wb.create_sheet("Weekly Retention")
    create_retention_sheet(ws_retention, RETENTION_DATA)

    return wb

def create_summary_sheet(ws):
    """Summary 시트 생성"""
    ws['A1'] = "Amplitude Report Summary"
    ws['A1'].font = Font(bold=True, size=16)
    ws.merge_cells('A1:D1')

    ws['A2'] = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ws['A2'].font = Font(italic=True, color="666666")

    # 메트릭 테이블
    headers = ["Metric", "Latest Value", "Previous Week", "Change"]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=4, column=col, value=header)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.border = BORDER
        cell.alignment = Alignment(horizontal='center')

    # WAU
    latest_wau = WAU_DATA["values"][-1]
    prev_wau = WAU_DATA["values"][-2]
    wau_change = ((latest_wau - prev_wau) / prev_wau * 100) if prev_wau else 0

    ws.cell(row=5, column=1, value="WAU").border = BORDER
    ws.cell(row=5, column=2, value=latest_wau).border = BORDER
    ws.cell(row=5, column=3, value=prev_wau).border = BORDER
    ws.cell(row=5, column=4, value=f"{wau_change:+.1f}%").border = BORDER

    # NAU
    latest_nau = NAU_DATA["values"][-1]
    prev_nau = NAU_DATA["values"][-2]
    nau_change = ((latest_nau - prev_nau) / prev_nau * 100) if prev_nau else 0

    ws.cell(row=6, column=1, value="NAU").border = BORDER
    ws.cell(row=6, column=2, value=latest_nau).border = BORDER
    ws.cell(row=6, column=3, value=prev_nau).border = BORDER
    ws.cell(row=6, column=4, value=f"{nau_change:+.1f}%").border = BORDER

    # Week 1 Retention
    ws.cell(row=7, column=1, value="Week 1 Retention").border = BORDER
    ws.cell(row=7, column=2, value="58.38%").border = BORDER
    ws.cell(row=7, column=3, value="-").border = BORDER
    ws.cell(row=7, column=4, value="-").border = BORDER

    # 컬럼 너비 조정
    ws.column_dimensions['A'].width = 18
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 12

def create_timeseries_sheet(ws, title, data):
    """시계열 데이터 시트 생성"""
    ws['A1'] = title
    ws['A1'].font = Font(bold=True, size=14)
    ws.merge_cells('A1:B1')

    # 헤더
    headers = ["Date", "Value"]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col, value=header)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.border = BORDER
        cell.alignment = Alignment(horizontal='center')

    # 데이터
    for row, (date, value) in enumerate(zip(data["dates"], data["values"]), 4):
        ws.cell(row=row, column=1, value=date).border = BORDER
        ws.cell(row=row, column=2, value=value).border = BORDER

    # 컬럼 너비 조정
    ws.column_dimensions['A'].width = 15
    ws.column_dimensions['B'].width = 12

def create_region_sheet(ws, title, data):
    """지역별 비교 시계열 시트 생성 (한국 vs 한국 외)"""
    ws['A1'] = title
    ws['A1'].font = Font(bold=True, size=14)
    ws.merge_cells('A1:D1')

    headers = ["Date", "South Korea", "Non-Korea", "Non-Korea %"]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col, value=header)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.border = BORDER
        cell.alignment = Alignment(horizontal='center')

    for row, (date, kr, non_kr) in enumerate(zip(data["dates"], data["korea"], data["non_korea"]), 4):
        total = kr + non_kr
        share = (non_kr / total * 100) if total else 0
        ws.cell(row=row, column=1, value=date).border = BORDER
        ws.cell(row=row, column=2, value=kr).border = BORDER
        ws.cell(row=row, column=3, value=non_kr).border = BORDER
        ws.cell(row=row, column=4, value=f"{share:.2f}%").border = BORDER

    for col, width in [('A', 15), ('B', 14), ('C', 14), ('D', 14)]:
        ws.column_dimensions[col].width = width


def create_retention_sheet(ws, data):
    """리텐션 시트 생성"""
    ws['A1'] = "Weekly Retention (Cohort Analysis)"
    ws['A1'].font = Font(bold=True, size=14)
    ws.merge_cells('A1:F1')

    # 도움말 섹션
    help_texts = [
        "[ 읽는 방법 ]",
        "• 각 행은 특정 주에 처음 방문한 사용자 그룹(코호트)입니다.",
        "• Week 0: 첫 방문 주에 활동한 사용자 수 (항상 100%)",
        "• Week 1, 2, 3...: 첫 방문 후 1주, 2주, 3주 뒤에 다시 돌아온 사용자 수",
        "• Overall 행: 전체 코호트의 평균 리텐션율",
        "",
        "예) Dec 22, 2025 코호트가 Week 2에 306명 → 12월 22일 주에 처음 온 465명 중 306명(65.8%)이 2주 후에도 활동"
    ]

    help_start_row = 3
    for i, text in enumerate(help_texts):
        cell = ws.cell(row=help_start_row + i, column=1, value=text)
        if i == 0:
            cell.font = Font(bold=True, color="4472C4")
        else:
            cell.font = Font(color="666666")
        ws.merge_cells(f'A{help_start_row + i}:G{help_start_row + i}')

    # 데이터 작성 (도움말 아래로 이동)
    data_start_row = help_start_row + len(help_texts) + 1
    for row_idx, row_data in enumerate(data, data_start_row):
        for col_idx, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border = BORDER
            if row_idx == data_start_row:  # 헤더
                cell.fill = HEADER_FILL
                cell.font = HEADER_FONT
                cell.alignment = Alignment(horizontal='center')

    # 컬럼 너비 조정
    ws.column_dimensions['A'].width = 14
    ws.column_dimensions['B'].width = 14
    ws.column_dimensions['C'].width = 10
    for i in range(4, 21):
        ws.column_dimensions[get_column_letter(i)].width = 10

def main():
    wb = create_workbook()

    # 폴더 생성 (없으면)
    os.makedirs(EXPORT_DIR, exist_ok=True)

    # 파일 저장
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f'amplitude_report_{today}.xlsx'
    filepath = os.path.join(EXPORT_DIR, filename)
    wb.save(filepath)
    print(f"Excel file created: {filepath}")

if __name__ == "__main__":
    main()
