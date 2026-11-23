import openpyxl

# 打开Excel
workbook = openpyxl.load_workbook("机票Agent测试用例_30条.xlsx")
sheet = workbook["测试用例"]

# 三条模拟测试结果
test_results = [
    {
        "actual": "航班查询成功，没有调用购买工具",
        "status": "Pass"
    },
    {
        "actual": "Agent调用了购买工具",
        "status": "Fail"
    },
    {
        "actual": "航班查询成功，没有调用购买工具",
        "status": "Pass"
    }
]

# 批量写入
for row, result in enumerate(test_results,start=2):

    sheet.cell(row=row, column=10).value = result["actual"]

    sheet.cell(row=row, column=11).value = result["status"]

# 保存为新文件
workbook.save("批量测试结果.xlsx")

print("批量写入完成！")




