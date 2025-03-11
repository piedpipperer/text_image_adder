from xlutils.copy import copy
from xlrd import open_workbook


combinations = {"2024": list(range(1, 13)), "2025": list(range(1, 4))}

# load excel file
rb = open_workbook(filename="excels/FACTURA_PIS_703.xls", formatting_info=True)

# open workbook
# sheet = workbook.active

for year in combinations:
    for index, month in enumerate(combinations[year]):
        # year = 2024
        # month

        wb = copy(rb)
        w_sheet = wb.get_sheet(0)

        # row number = 0 , colu"mn number = 1
        w_sheet.write(14, 0, f"L-{year}-{index+1}")
        w_sheet.write(14, 1, f"01/{month}/{year}")

        for i in range(1, 7):
            col = w_sheet.col(i)
            col.width = 256 * 15
        # save the file
        wb.save(f"generated_excels/FACTURA_{year}_{month}.xlsx")
