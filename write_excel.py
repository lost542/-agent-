import openpyxl

# 打开Excel文件
workbook = openpyxl.load_workbook("机票Agent测试用例_30条.xlsx")

# 选择工作表
sheet = workbook["测试用例"]

# 写入实际结果（J列）
sheet.cell(row=5, column=10).value = "查询成功"

# 写入测试状态（K列）
sheet.cell(row=5, column=11).value = "Pass"

# 保存Excel文件
workbook.save("测试结果.xlsx")

print("Excel写入成功！")