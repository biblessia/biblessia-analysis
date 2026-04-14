#!/usr/bin/env python3
"""Amplitude 데이터를 Excel로 내보내기"""

import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime

# 내보내기 폴더 설정
EXPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")

# 데이터 정의 (Amplitude에서 가져온 데이터 - 2026-04-15 업데이트)
WAU_DATA = {
    "dates": ["2025-10-27","2025-11-03","2025-11-10","2025-11-17","2025-11-24","2025-12-01","2025-12-08","2025-12-15","2025-12-22","2025-12-29","2026-01-05","2026-01-12","2026-01-19","2026-01-26","2026-02-02","2026-02-09","2026-02-16","2026-02-23","2026-03-02","2026-03-09","2026-03-16","2026-03-23","2026-03-30","2026-04-06"],
    "values": [806,1100,1163,1198,1152,1097,1095,1084,1348,2010,2074,2002,2028,2118,2270,2222,2138,2407,2723,2918,2881,2914,2961,2908]
}

NAU_DATA = {
    "dates": ["2025-10-27","2025-11-03","2025-11-10","2025-11-17","2025-11-24","2025-12-01","2025-12-08","2025-12-15","2025-12-22","2025-12-29","2026-01-05","2026-01-12","2026-01-19","2026-01-26","2026-02-02","2026-02-09","2026-02-16","2026-02-23","2026-03-02","2026-03-09","2026-03-16","2026-03-23","2026-03-30","2026-04-06"],
    "values": [315,409,295,243,172,126,164,152,465,705,373,251,255,320,352,224,223,374,392,497,352,295,312,354]
}

RETENTION_DATA = [
    ["Segment", "Start Date", "Users", "Week 0", "Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6", "Week 7", "Week 8", "Week 9", "Week 10", "Week 11", "Week 12", "Week 13", "Week 14", "Week 15", "Week 16"],
    ["South Korea", "Overall", "Retained", 5744, 3295, 2632, 2290, 1940, 1693, 1420, 1201, 1135, 1016, 892, 790, 665, 601, 451, 199, 167],
    ["South Korea", "Overall", "Retained %", "100.0%", "61.13%", "51.83%", "47.88%", "43.78%", "43.04%", "40.09%", "37.91%", "38.54%", "37.34%", "37.65%", "38.56%", "37.07%", "38.95%", "38.55%", "42.8%", "35.91%"],
    ["South Korea", "Apr 06, 2026", 354, 354, 185],
    ["South Korea", "Mar 30, 2026", 312, 312, 148, 93],
    ["South Korea", "Mar 23, 2026", 295, 295, 163, 134, 67],
    ["South Korea", "Mar 16, 2026", 352, 352, 200, 157, 132, 83],
    ["South Korea", "Mar 09, 2026", 497, 497, 283, 237, 226, 183, 120],
    ["South Korea", "Mar 02, 2026", 392, 392, 257, 209, 202, 176, 171, 95],
    ["South Korea", "Feb 23, 2026", 374, 374, 238, 186, 167, 160, 139, 124, 87],
    ["South Korea", "Feb 16, 2026", 223, 223, 127, 109, 97, 92, 99, 96, 86, 52],
    ["South Korea", "Feb 09, 2026", 224, 224, 134, 112, 121, 97, 94, 97, 87, 81, 67],
    ["South Korea", "Feb 02, 2026", 352, 352, 209, 171, 148, 145, 132, 121, 111, 111, 104, 70],
    ["South Korea", "Jan 26, 2026", 320, 320, 187, 146, 138, 117, 137, 120, 106, 104, 103, 96, 68],
    ["South Korea", "Jan 19, 2026", 255, 255, 130, 121, 107, 92, 86, 89, 74, 78, 73, 81, 71, 45],
    ["South Korea", "Jan 12, 2026", 251, 251, 143, 120, 111, 99, 87, 85, 83, 83, 72, 67, 74, 70, 47],
    ["South Korea", "Jan 05, 2026", 373, 373, 240, 192, 172, 162, 148, 133, 137, 142, 145, 135, 130, 121, 112, 82],
    ["South Korea", "Dec 29, 2025", 705, 705, 491, 431, 397, 361, 348, 323, 291, 310, 296, 295, 289, 272, 277, 253, 199],
    ["South Korea", "Dec 22, 2025", 465, 465, 345, 307, 272, 256, 252, 232, 226, 226, 223, 218, 226, 202, 212, 198, 199, 167],
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
