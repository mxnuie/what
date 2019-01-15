import xlrd

data = xlrd.open_workbook(r"C:\Users\65433\Desktop\shuju.xlsx")
table = data.sheet_by_index(0)
rows_count = table.nrows
print(rows_count)
