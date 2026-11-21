import json
from deepseek_test import extract_lowest_price

# 1. 读取测试用例黄金集
with open("test_cases.json", "r", encoding="utf-8") as file:
    test_cases = json.load(file)

# 2. 每条用例连续跑 3 次
run_times = 3

# 记录所有结果
consistency_results = []

for case in test_cases:
    case_id = case["case_id"]
    expected_price = case["expected_price"]

    prices = []       # 记录 3 次提取的价格
    errors = []       # 记录出错信息

    for i in range(run_times):
        result = extract_lowest_price(case["final_output"])

        if result["status"] == "ERROR":
            prices.append(None)
            errors.append(result["error"])
        else:
            prices.append(result["price"])

    # 判断 3 次结果是否一致：全部等于第 1 次才算一致
    is_consistent = all(p == prices[0] for p in prices)

    consistency_results.append({
        "case_id": case_id,
        "expected_price": expected_price,
        "prices": prices,
        "is_consistent": is_consistent,
        "errors": errors
    })

    print("用例：", case_id)
    print("预期价格：", expected_price)
    print("三次结果：", prices)
    print("是否一致：", is_consistent)
    print("----------------------")

# 3. 统计

# 3.1 一致性：一致的用例数 + 不一致的用例编号
consistent_count = 0
inconsistent_cases = []

for r in consistency_results:
    if r["is_consistent"]:
        consistent_count += 1
    else:
        inconsistent_cases.append(r["case_id"])

# 3.2 总准确率：13 条 × 3 次 = 39 次里，提取价与预期价相同的次数
correct_count = 0
total_count = 0
wrong_cases = []

for r in consistency_results:
    for p in r["prices"]:
        total_count += 1
        if p == r["expected_price"]:
            correct_count += 1
        else:
            wrong_cases.append((r["case_id"], p, r["expected_price"]))

accuracy = correct_count / total_count * 100 if total_count > 0 else 0

# 3.3 出错的用例编号
error_cases = [r["case_id"] for r in consistency_results if len(r["errors"]) > 0]

# 4. 输出报告
print("\n========== 裁判一致性报告 ==========")
print("用例总数：", len(consistency_results))
print("每条跑的次数：", run_times)
print("总调用次数：", total_count)
print("一致的用例数：", consistent_count)
print("不一致的用例数：", len(inconsistent_cases))
print("总体准确率：", round(accuracy, 2), "%")
print("不一致用例：", inconsistent_cases)
print("出错用例：", error_cases)
print("预测错误明细（用例, 实际, 预期）：", wrong_cases)
print("=====================================")
