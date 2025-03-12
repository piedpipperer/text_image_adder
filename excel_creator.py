from xlutils.copy import copy
from xlrd import open_workbook
from xlwt import XFStyle
from argparse import ArgumentParser

combinations = {"2024": list(range(1, 6))}
combinations2 = {"2024": list(range(7, 13)), "2025": list(range(1, 4))}
new_combinations = [{"date_interval": combinations, "importe": 204}, {"date_interval": combinations2, "importe": 208}]

rb = open_workbook(filename="excels/FACTURA_PIS_703.xls", formatting_info=True)


def generate_invoices(year_filter=None, month_filter=None):
    for combination in new_combinations:
        for year in combination["date_interval"]:
            for index, month in enumerate(combination["date_interval"][year]):
                if (year_filter is None or year_filter == str(year)) and (
                    month_filter is None or month_filter == str(month)
                ):
                    wb = copy(rb)
                    w_sheet = wb.get_sheet(0)
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
                    wb.save(f"generated_excels/FACTURAS/{year}-{month}.xlsx")


if __name__ == "__main__":
    parser = ArgumentParser(description="bill rent creator")
    parser.add_argument("--year", type=str, help="year filter for invoices")
    parser.add_argument("--month", type=str, help="month filter for invoices")
    args = parser.parse_args()
    generate_invoices(year_filter=args.year, month_filter=args.month)
