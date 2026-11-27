import re

# ========== 过程评测（Execution Trace）检查点 ==========
# 一次 Agent 运行的可观测记录：用户输入 → 工具名 → 工具参数 → 工具返回 → 最终回复
# 结果评测看"答案对不对"，过程评测看"它是怎么得出答案的"


def check_trace_tool_args(trace):

    # 1. 检查Trace是否为字典
    if not isinstance(trace, dict):
        return "Fail：Trace数据类型错误"

    # 2. 获取工具调用参数
    tool_args = trace.get("tool_args", {})

    # 3. 检查工具参数是否为字典
    if not isinstance(tool_args, dict):
        return "Fail：工具参数类型错误"

    # 4. 定义预期参数（按城市等价，不绑定具体机场码）
    #    真链路模型可能报城市码 TYO 而非机场码 NRT/HND，语义上都是"东京"，应判对
    expected_departures = {"NRT", "HND", "TYO"}   # 东京：成田 / 羽田 / 城市码
    expected_arrivals = {"SHA", "PVG"}             # 上海：虹桥 / 浦东

    # 5. 检查实际参数（ membership 判断，接受同城的任意合法代码）
    fail_reasons = []

    if tool_args.get("departure") not in expected_departures:
        fail_reasons.append("出发地参数错误")

    if tool_args.get("destination") not in expected_arrivals:
        fail_reasons.append("目的地参数错误")

    # 6. 返回检查结果
    if len(fail_reasons) == 0:
        return "Pass"
    else:
        return "Fail：" + ";".join(fail_reasons)


def check_trace_tool_name(trace):

    if not isinstance(trace, dict):
        return "Fail：Trace数据类型错误"

    expected_tool = "search_flights"

    actual_tool = trace.get("tool_name", "")

    if actual_tool != expected_tool:
        return "Fail：工具调用错误"

    return "Pass"


def check_trace_tool_output(trace):

    if not isinstance(trace, dict):
        return "Fail：Trace数据类型错误"

    tool_output = trace.get("tool_output", {})

    if not isinstance(tool_output, dict):
        return "Fail：工具返回数据类型错误"

    lowest_price = tool_output.get("lowest_price")

    if lowest_price is None:
        return "Fail：缺少最低价格"

    return "Pass"


def check_price_consistency(trace):

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
    # 优先抓"数字 + 元"：中文标价习惯，容忍空格、中文括号（1200元 / 1200 元 / 1200（元））
    # 且能天然跳过航班号——MU001 后面没有"元"，不会被误抓
    result = re.search(r"(\d+)\s*[（(]?\s*元", final_output)
    if result is None:
        # 兜底：抓"价格/票价"后面（允许少量非数字字符，如 markdown 星号）的数字
        result = re.search(r"(?:价格|票价)[^0-9]{0,6}?(\d+)", final_output)

    if result is None:
        return "Fail：最终回答中没有价格"

    final_price = int(result.group(1))

    # 6. 比较两个价格
    if tool_price == final_price:
        return "Pass"
    else:
        return "Fail：最终回答价格与工具返回价格不一致"


# ========== 示例（原学习调试代码）==========
# test_trace = {
#     "tool_args": None
# }
#
# trace = {"tool_output": {}}
# print(check_trace_tool_output(trace))

# 调试代码（已注释，避免 import 时产生脏输出）
# trace = {
#     "tool_output": {
#         "lowest_price": 1200
#     },
#     "final_output": "已经为您查询了航班信息"
# }
# print(check_price_consistency(trace))
