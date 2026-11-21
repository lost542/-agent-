import json
from deepseek_test import extract_lowest_price

# 1. 读取测试用例
with open("test_cases.json", "r", encoding="utf-8") as file:
    test_cases = json.load(file)

# 2. 准备统计数据
results = []

# 3. 遍历所有测试用例
for case in test_cases:

    case_id = case["case_id"]
    final_output = case["final_output"]
    expected_price = case["expected_price"]

    print("正在执行：", case_id)

    # 4. 调用DeepSeek语义识别函数
    actual_result = extract_lowest_price(final_output)

    # 5. 获取实际识别价格
    actual_price = actual_result["price"]

    # 6. 判断测试结果
    if actual_result["status"] == "ERROR":
        test_status = "ERROR"

    elif actual_price == expected_price:
        test_status = "PASS"

    else:
        test_status = "FAIL"

    # 7. 保存单条测试结果
    results.append({
        "case_id": case_id,
        "expected_price": expected_price,
        "actual_price": actual_price,
        "status": test_status,
        "error": actual_result["error"]
    })

    print("实际价格：", actual_price)
    print("测试状态：", test_status)
    print("----------------------")

print("全部测试完成！")
print("测试结果：", results)

# 8. 初始化统计数量
pass_count = 0
fail_count = 0
error_count = 0

# 9. 遍历测试结果
for result in results:

    if result["status"] == "PASS":
        pass_count += 1

    elif result["status"] == "FAIL":
        fail_count += 1

    elif result["status"] == "ERROR":
        error_count += 1

# 10. 计算通过率
total_count = len(results)

if total_count > 0:
    pass_rate = pass_count / total_count * 100
else:
    pass_rate = 0

# 11. 输出统计报告
print("\n========== 自动化评测报告 ==========")
print("总测试数量：", total_count)
print("PASS数量：", pass_count)
print("FAIL数量：", fail_count)
print("ERROR数量：", error_count)
print("测试通过率：", round(pass_rate, 2), "%")
print("====================================")