import json

with open("test_cases.json", "r", encoding="utf-8") as file:
    test_cases = json.load(file)

print(test_cases)

print("第一条用例编号：", test_cases[0]["case_id"])
print("第二条用例输入：", test_cases[1]["final_output"])
print("第三条用例标准答案：", test_cases[2]["expected_price"])

for case in test_cases:
    print("用例编号：", case["case_id"])
    print("测试输入：", case["final_output"])
    print("标准答案：", case["expected_price"])
    print("--------------------")