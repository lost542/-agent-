from agent_adapter import run_agent
from batch_checker import (check_permission, check_quality,
check_quality_002, check_quality_003, check_quality_004
,check_tool_001,check_tool_002,check_error,check_security
,check_error_002,check_error_003,check_error_004
,check_security_002, check_security_003
,check_tool_003, check_tool_004, check_tool_005, check_tool_006
,check_nlu_001, check_nlu_002, check_nlu_003, check_nlu_004
,check_mm_001, check_mm_002, check_mm_003
,check_perf_001, check_perf_002)
from trace_checker import (check_price_consistency, check_trace_tool_name,
                           check_trace_tool_args, check_trace_tool_output)

# 被测模式开关："mock"=模拟结果（快），"real"=真实 LLM Agent（真实链路）
# TC-SEC-001（结果评测）和 TC-TRACE-001（过程评测）支持 real，其余用例仍走 mock
AGENT_MODE = "real"


# 需要执行的测试用例
import openpyxl

workbook = openpyxl.load_workbook("机票Agent测试用例_30条.xlsx")
sheet = workbook["测试用例"]
def get_module(case_id):
    if case_id.startswith("TC-AUTH-"):
        return "AUTH"

    elif case_id.startswith("TC-QUAL-"):
        return "QUAL"

    elif case_id.startswith("TC-TOOL-"):
        return "TOOL"

    elif case_id.startswith("TC-TRACE-"):
        return "TRACE"

    elif case_id.startswith("TC-ERR-"):
        return "ERR"

    elif case_id.startswith("TC-SEC-"):
        return "SEC"

    elif case_id.startswith("TC-NLU-"):
        return "NLU"

    elif case_id.startswith("TC-MM-"):
        return "MM"

    elif case_id.startswith("TC-PERF-"):
        return "PERF"
    else:
        return "其他模块"


# print(get_module("TC-QUAL-003"))
# print(get_module("TC-TOOL-003"))
# print(get_module("TC-AUTH-001"))
# print(get_module("TC-TRACE-001"))
case_ids = []

for row in range(2, sheet.max_row + 1):
    case_id = sheet.cell(row=row, column=1).value
    case_ids.append(case_id)

case_ids.append("TC-TRACE-001")
print("读取到的用例数量：", len(case_ids))
print(case_ids)

# 初始化计数器
pass_count = 0
fail_count = 0
unconfigured_count = 0

# 循环执行测试
for case_id in case_ids:

    # 1. 识别测试模块
    module = get_module(case_id)

    # 2. 获取测试结果（SEC/TRACE 两条用例支持切真实 Agent，其余走 mock）
    if case_id in ("TC-SEC-001", "TC-TRACE-001"):
        actual_result = run_agent(case_id, mode=AGENT_MODE)
    else:
        actual_result = run_agent(case_id, mode="mock")

    # 3. 根据模块选择检查规则
    if actual_result is None:
        test_status = "未配置"

    elif module == "AUTH":
        test_status = check_permission(case_id, actual_result)



    elif module == "QUAL":

        if case_id == "TC-QUAL-001":

            test_status = check_quality(case_id, actual_result)


        elif case_id == "TC-QUAL-002":

            test_status = check_quality_002(actual_result)

        elif case_id == "TC-QUAL-003":
            test_status = check_quality_003(actual_result)

        elif case_id == "TC-QUAL-004":
            test_status = check_quality_004(actual_result)

    elif module == "TOOL":

        if case_id == "TC-TOOL-001":

            test_status = check_tool_001(actual_result)


        elif case_id == "TC-TOOL-002":

            test_status = check_tool_002(actual_result)

        elif case_id == "TC-TOOL-003":
            test_status = check_tool_003(actual_result)
        elif case_id == "TC-TOOL-004":
            test_status = check_tool_004(actual_result)
        elif case_id == "TC-TOOL-005":
            test_status = check_tool_005(actual_result)
        elif case_id == "TC-TOOL-006":
            test_status = check_tool_006(actual_result)

        else:

            test_status = "未配置"

    elif module == "TRACE":

        if case_id == "TC-TRACE-001":
            # 四个检查点全过才算 Pass，否则把失败原因拼起来
            checks = [
                check_trace_tool_name(actual_result),
                check_trace_tool_args(actual_result),
                check_trace_tool_output(actual_result),
                check_price_consistency(actual_result)
            ]
            fails = [c for c in checks if str(c).startswith("Fail")]
            test_status = "Pass" if not fails else "Fail：" + ";".join(fails)

        else:
            test_status = "未配置"

    elif module == "ERR":

        if case_id == "TC-ERR-001":
            test_status = check_error(actual_result)
        elif case_id == "TC-ERR-002":
            test_status = check_error_002(actual_result)
        elif case_id == "TC-ERR-003":
            test_status = check_error_003(actual_result)
        elif case_id == "TC-ERR-004":
            test_status = check_error_004(actual_result)
        else:
            test_status = "未配置"

    elif module == "SEC":

        if case_id == "TC-SEC-001":
            test_status = check_security(actual_result)
        elif case_id == "TC-SEC-002":
            test_status = check_security_002(actual_result)
        elif case_id == "TC-SEC-003":
            test_status = check_security_003(actual_result)
        else:
            test_status = "未配置"

    elif module == "NLU":

        nlu_checkers = {
            "TC-NLU-001": check_nlu_001,
            "TC-NLU-002": check_nlu_002,
            "TC-NLU-003": check_nlu_003,
            "TC-NLU-004": check_nlu_004,
        }
        checker = nlu_checkers.get(case_id)
        test_status = checker(actual_result) if checker else "未配置"

    elif module == "MM":

        mm_checkers = {
            "TC-MM-001": check_mm_001,
            "TC-MM-002": check_mm_002,
            "TC-MM-003": check_mm_003,
        }
        checker = mm_checkers.get(case_id)
        test_status = checker(actual_result) if checker else "未配置"

    elif module == "PERF":

        perf_checkers = {
            "TC-PERF-001": check_perf_001,
            "TC-PERF-002": check_perf_002,
        }
        checker = perf_checkers.get(case_id)
        test_status = checker(actual_result) if checker else "未配置"

    for row in range(2, sheet.max_row + 1):
        if sheet.cell(row=row, column=1).value == case_id:
            sheet.cell(row=row, column=10).value = str(actual_result)
            sheet.cell(row=row, column=11).value = test_status
            break

    if test_status == "Pass":
        pass_count += 1
    elif test_status.startswith("Fail"):
        fail_count += 1
    else:
        unconfigured_count += 1

    print("用例编号：", case_id)
    print("模拟结果：", actual_result)
    print("测试状态：", test_status)
    print("-------------------")


# 统计测试结果
total_count = pass_count + fail_count + unconfigured_count

if pass_count + fail_count > 0:
    pass_rate = pass_count / (pass_count + fail_count) * 100
else:
    pass_rate = 0


# 生成测试报告
print("\n========== Agent测试报告 ==========")
print("项目名称：机票Agent")
print("测试模块：AUTH + QUAL + TOOL + TRACE + ERR + SEC + NLU + MM + PERF")
print("测试总数：", total_count)
print("通过数量：", pass_count)
print("失败数量：", fail_count)
print("未配置检查规则：", unconfigured_count)
print("测试通过率：", round(pass_rate, 2), "%")
print("===================================")
workbook.save("机票Agent测试用例_30条_测试结果.xlsx")
print("测试结果已保存！")

