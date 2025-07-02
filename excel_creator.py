from xlutils.copy import copy
from xlrd import open_workbook
from xlwt import XFStyle
from argparse import ArgumentParser
import os

COMBINATIONS = {2024: list(range(1, 6))}
COMBINATIONS2 = {2024: list(range(7, 13)), 2025: list(range(1, 4))}
NEW_COMBINATIONS = [{"date_interval": COMBINATIONS, "importe": 204}, {"date_interval": COMBINATIONS2, "importe": 208}]


def generate_invoices(year_filter=None, month_filter=None):
    rb = open_workbook(filename="excels/FACTURA_PIS_703.xls", formatting_info=True)
    wb = copy(rb)
    w_sheet = wb.get_sheet(0)
    for combination in NEW_COMBINATIONS:
        for year in combination["date_interval"]:
            for index, month in enumerate(combination["date_interval"][year]):
                if (year_filter is None or year_filter == str(year)) and (
                    month_filter is None or month_filter == str(month)
                ):
                    w_sheet.write(14, 0, f"L-{year}-{index+1}")
                    w_sheet.write(14, 1, f"01/{month}/{year}")
                    style = XFStyle()
                    style.num_format_str = "0.00"
                    w_sheet.write(19, 4, combination["importe"], style)
                    w_sheet.write(29, 4, combination["importe"], style)
                    w_sheet.write(38, 4, combination["importe"], style)
                    for i in range(1, 7):
                        col = w_sheet.col(i)
                        col.width = 256 * 15
                    year_folder = f"generated_excels/FACTURAS/{year}"
                    if not os.path.exists(year_folder):
                        os.makedirs(year_folder)
                    wb.save(f"{year_folder}/{month}.xlsx")


def generate_invoices2(
    year_filter=None,
    month_filter=None,
    output_dir: str = "generated_excels/FACTURAS",
    excel_file: str = "excels/FACTURA_PIS_703.xls",
):
    rb = open_workbook(filename=excel_file, formatting_info=True)
    wb = copy(rb)
    w_sheet = wb.get_sheet(0)

    for combination in NEW_COMBINATIONS:
        for year in combination["date_interval"]:
            for index, month in enumerate(combination["date_interval"][year]):
                if (year_filter is None or year_filter == str(year)) and (
                    month_filter is None or month_filter == str(month)
                ):
                    w_sheet.write(14, 0, f"L-{year}-{index+1}")
                    w_sheet.write(14, 1, f"01/{month}/{year}")
                    style = XFStyle()
                    style.num_format_str = "0.00"
                    w_sheet.write(19, 4, combination["importe"], style)
                    w_sheet.write(29, 4, combination["importe"], style)
                    w_sheet.write(38, 4, combination["importe"], style)
                    for i in range(1, 7):
                        col = w_sheet.col(i)
                        col.width = 256 * 15
                    year_folder = os.path.join(output_dir, str(year))
                    if not os.path.exists(year_folder):
                        os.makedirs(year_folder)
                    wb.save(os.path.join(year_folder, f"{month}.xlsx"))


if __name__ == "__main__":
    parser = ArgumentParser(description="bill rent creator")
    parser.add_argument("--year", type=str, help="year filter for invoices")
    parser.add_argument("--month", type=str, help="month filter for invoices")
    args = parser.parse_args()
    generate_invoices2(year_filter=args.year if args.year else None, month_filter=args.month if args.month else None)
