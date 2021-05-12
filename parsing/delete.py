import sys
from openpyxl import load_workbook

# Deletes the first row in every sheet in the spreadsheet shifting up.
def main(xlfile):
    wb = load_workbook(filename=xlfile)
    for ws in wb.worksheets:
        ws.delete_rows(0)
    wb.save(xlfile)

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        exit("Usage: python3 delete.py path/to/spreadsheet.xlsx")

    sys.exit(main(args[0]))
