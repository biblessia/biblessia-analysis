#!/usr/bin/env python3
"""Amplitude 데이터를 Excel로 내보내기"""

import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime

# 내보내기 폴더 설정
EXPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")

# 데이터 정의 (Amplitude에서 가져온 데이터 - 2026-01-13 업데이트)
WAU_DATA = {
    "dates": ["2025-07-28","2025-08-04","2025-08-11","2025-08-18","2025-08-25","2025-09-01","2025-09-08","2025-09-15","2025-09-22","2025-09-29","2025-10-06","2025-10-13","2025-10-20","2025-10-27","2025-11-03","2025-11-10","2025-11-17","2025-11-24","2025-12-01","2025-12-08","2025-12-15","2025-12-22","2025-12-29","2026-01-05","2026-01-12"],
    "values": [185,226,231,261,293,421,490,528,526,500,446,535,545,806,1100,1163,1196,1151,1097,1093,1078,1347,2003,2061,1194]
}

NAU_DATA = {
    "dates": ["2025-07-28","2025-08-04","2025-08-11","2025-08-18","2025-08-25","2025-09-01","2025-09-08","2025-09-15","2025-09-22","2025-09-29","2025-10-06","2025-10-13","2025-10-20","2025-10-27","2025-11-03","2025-11-10","2025-11-17","2025-11-24","2025-12-01","2025-12-08","2025-12-15","2025-12-22","2025-12-29","2026-01-05","2026-01-12"],
    "values": [84,79,50,55,90,150,117,103,81,65,73,74,68,315,409,295,243,171,127,165,150,465,705,373,62]
}

RETENTION_DATA = [
    ["Segment", "Start Date", "Users", "Week 0", "Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6", "Week 7", "Week 8", "Week 9", "Week 10", "Week 11", "Week 12", "Week 13", "Week 14", "Week 15", "Week 16"],
    ["South Korea", "Overall", "Retained", 3779, 2182, 1436, 953, 801, 640, 534, 439, 362, 295, 175, 99, 81, 55, 37, 14, 8],
    ["South Korea", "Overall", "Retained %", "100.0%", "64.06%", "53.17%", "42.62%", "38.4%", "33.32%", "29.77%", "27.05%", "26.23%", "27.19%", "25.89%", "27.42%", "27.65%", "25.11%", "25.34%", "17.28%", "9.88%"],
    ["South Korea", "Jan 12, 2026", 62, 62],
    ["South Korea", "Jan 05, 2026", 373, 373, 162],
    ["South Korea", "Dec 29, 2025", 705, 705, 489, 316],
    ["South Korea", "Dec 22, 2025", 465, 465, 344, 306, 201],
    ["South Korea", "Dec 15, 2025", 150, 150, 76, 75, 69, 36],
    ["South Korea", "Dec 08, 2025", 165, 165, 89, 85, 84, 84, 54],
    ["South Korea", "Dec 01, 2025", 127, 127, 59, 45, 34, 34, 41, 20],
    ["South Korea", "Nov 24, 2025", 171, 171, 92, 78, 66, 62, 59, 47, 20],
    ["South Korea", "Nov 17, 2025", 243, 243, 150, 122, 102, 96, 77, 80, 74, 38],
    ["South Korea", "Nov 10, 2025", 295, 295, 168, 145, 119, 96, 86, 73, 78, 61, 33],
    ["South Korea", "Nov 03, 2025", 409, 409, 252, 216, 163, 161, 135, 123, 92, 119, 107, 46],
    ["South Korea", "Oct 27, 2025", 315, 315, 235, 181, 147, 116, 102, 89, 83, 66, 72, 66, 18],
    ["South Korea", "Oct 20, 2025", 68, 68, 46, 35, 31, 29, 23, 20, 20, 20, 20, 21, 23, 13],
    ["South Korea", "Oct 13, 2025", 74, 74, 48, 40, 36, 32, 32, 28, 25, 25, 25, 20, 19, 22, 11],
    ["South Korea", "Oct 06, 2025", 73, 73, 50, 39, 37, 34, 35, 33, 24, 30, 31, 28, 22, 23, 20, 8],
    ["South Korea", "Sep 29, 2025", 65, 65, 39, 35, 27, 28, 27, 22, 22, 22, 24, 25, 23, 21, 21, 24, 9],
    ["South Korea", "Sep 22, 2025", 81, 81, 45, 34, 38, 29, 23, 19, 21, 19, 16, 15, 12, 15, 14, 13, 14, 8],
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
    ws.cell(row=7, column=2, value="64.06%").border = BORDER
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
