# a='李紫阳'
# b='李紫阳太帅了'
#
# if a in b:
#     print("你是天才")
# else:
#     print("你不是天才")
#
#
# # fail_reasons 是一个列表，存多条失败理由
# fail_reasons = [
#     "参数错误：传入HND，用户要求NRT成田机场",
#     "结果幻觉：tool_output=1200，final_output写成1500"
# ]
# print(type(fail_reasons))
# # 用换行拼接
# res = "?".join(fail_reasons)
# print(res,type(res))


import re

# final_output = "最低价格是1500元"
#
# result = re.search(r"\d+", final_output)
#
# print(result.group())
#
# import re
#
# answer = "这张机票的价格是 1580 元"
#
# price = re.findall(r"\d+", answer)
#
# print(price)


# text = "TC-001、AB-002、TC-003、AB-004、CD-005"
# import re
# result = re.findall(r"TC-[0-9]+|AB-[0-9]+", text)
# print(result)
# import re
#
# answer = "本次测试结果：PASS"
#
#
# if re.search(r"^PASS$", answer):
#     print("格式正确")
# else:
#     print("格式错误")
import re

log = """
TC-001, 结果: PASS
TC-002, 结果: FAIL
TC-003, 结果: PASS
TC-004, 结果: PASS
TC-005, 结果: FAIL
TC-006, 结果: PASS
TC-007, 结果: PASS
TC-008, 结果: FAIL
"""

# 提取所有PASS用例编号
pass_list = re.findall(r'(TC-\d+), 结果: PASS', log)
# 提取所有FAIL用例编号
fail_list = re.findall(r'(TC-\d+), 结果: FAIL', log)

# 统计数量
# pass_count = len(pass_list)
# fail_count = len(fail_list)
# total_count = pass_count + fail_count
#
# # 计算通过率
# pass_rate = pass_count / total_count
#
# # 判断是否达到80%
# is_meet = pass_rate >= 0.8
#
# # 打印结果
# print("PASS用例：", pass_list)
# print("FAIL用例：", fail_list)
# print("成功数量：", pass_count)
# print("失败数量：", fail_count)
# print("总用例数：", total_count)
# print(f"通过率：{pass_rate:.2%}")
# print("通过率是否达到80%：", is_meet)

# test_results = ["PASS", "FAIL", "PASS", "FAIL", "PASS"]
#
# print(test_results[1])
# print(test_results[3])

# trace={"tool_output": {}}
# print(check_trace_tool_output(trace))


import re

def check_trace_consistency(trace):

    # 1. 检查Trace是否为字典
    if not isinstance(trace, dict):
        return "Fail：Trace数据类型错误"

    # 2. 获取工具返回结果
    tool_output = trace.get("tool_output", {})

    if not isinstance(tool_output, dict):
        return "Fail：工具返回结果类型错误"

    # 3. 获取工具返回价格
    tool_price = tool_output.get("lowest_price")

    if tool_price is None:
        return "Fail：缺少工具返回价格"

    # 4. 获取Agent最终回答
    final_output = trace.get("final_output", "")

    # 5. 提取最终回答中的价格
    result = re.search(r"\d+", final_output)

    if result is None:
        return "Fail：最终回答中没有价格"

    final_price = int(result.group())

    # 6. 比较两个价格
    if tool_price == final_price:
        return "Pass"
    else:
        return "Fail：最终回答价格与工具返回价格不一致"

trace = {
    "tool_output": {
        "lowest_price": 1200
    },
    "final_output": "最低价格是1200元"
}
print(check_trace_consistency(trace))
