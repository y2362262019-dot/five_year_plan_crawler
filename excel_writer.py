import os

import openpyxl

EXCEL_COLUMNS = [
    "省份", "城市", "序号", "城市代码", "所属地域", "胡焕庸线",
    "执行时间", "所属时期", "文章日期", "新网址", "备注", "本地路径", "抓取状态",
]


def create_workbook() -> openpyxl.Workbook:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(EXCEL_COLUMNS)
    # Freeze header
    ws.freeze_panes = "A2"
    # Header style
    header_font = openpyxl.styles.Font(bold=True)
    for col_idx in range(1, len(EXCEL_COLUMNS) + 1):
        ws.cell(row=1, column=col_idx).font = header_font
    return wb


def append_row(ws, row_data: dict, output_dir: str):
    values = [row_data.get(col, "") for col in EXCEL_COLUMNS]
    ws.append(values)


def save(wb: openpyxl.Workbook, output_dir: str):
    path = os.path.join(output_dir, "summary.xlsx")
    wb.save(path)
    return path
