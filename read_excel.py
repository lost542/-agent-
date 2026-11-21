import openpyxl
# 打开Excel文件
workbook = openpyxl.load_workbook("机票Agent测试用例_30条.xlsx")

# 选择工作表
sheet = workbook["测试用例"]

# 批量读取测试用例
for row in range(2, sheet.max_row + 1):

    # 读取测试用例编号
    case_id = sheet.cell(row=row, column=1).value

    # 读取测试输入
    test_input = sheet.cell(row=row, column=6).value

    # 读取预期结果
    expected_result = sheet.cell(row=row, column=8).value

    # 打印三个字段
    print("测试编号：", case_id)
    print("测试输入：", test_input)
    print("预期结果：", expected_result)
    print("-" * 40)
# # 写入测试结果
#     sheet.cell(row=row, column=10).value = "待执行"
#
# # 写入测试状态
#     sheet.cell(row=row, column=11).value = "Not Run"
#
# # 保存Excel文件
# workbook.save("机票Agent测试用例_30条.xlsx")