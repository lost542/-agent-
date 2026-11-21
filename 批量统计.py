
results = [
    {"status": "SUCCESS", "price": 1200, "expected_price": 1200, "error": None},
    {"status": "SUCCESS", "price": 1500, "expected_price": 1500, "error": None},
    {"status": "ERROR", "price": None, "expected_price": 1200, "error": "API超时"},
    {"status": "SUCCESS", "price": None, "expected_price": 1200, "error": None},
    {"status": "ERROR", "price": None, "expected_price": 1800, "error": "JSON解析失败"}
]

# 初始化计数器
success_count = 0
error_count = 0
unknown_price_count = 0
recognized_price_count = 0
pass_count = 0
fail_count = 0

# 遍历测试结果
for result in results:

    if result["status"] == "SUCCESS":
        success_count += 1

        if result["price"] is None:
            unknown_price_count += 1
            fail_count += 1
        else:
            recognized_price_count += 1

            if result["price"] == result["expected_price"]:
                pass_count += 1
            else:
                fail_count += 1

    elif result["status"] == "ERROR":
        error_count += 1

# 计算统计指标
total_count = len(results)

success_rate = success_count / total_count * 100

if success_count > 0:
    recognition_rate = recognized_price_count / success_count * 100
else:
    recognition_rate = 0

if success_count > 0:
    accuracy_rate = pass_count / success_count * 100
else:
    accuracy_rate = 0

# 输出统计报告
print("========== Agent评测统计报告 ==========")
print("总测试数量：", total_count)
print("程序成功数量：", success_count)
print("程序异常数量：", error_count)
print("成功识别价格数量：", recognized_price_count)
print("无法识别价格数量：", unknown_price_count)
print("PASS数量：", pass_count)
print("FAIL数量：", fail_count)

print("---------------------------------------")
print("程序运行成功率：", round(success_rate, 2), "%")
print("价格可识别率：", round(recognition_rate, 2), "%")
print("语义识别准确率：", round(accuracy_rate, 2), "%")
print("=======================================")
