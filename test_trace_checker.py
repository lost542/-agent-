from trace_checker import (
    check_trace_tool_args,
    check_trace_tool_name,
    check_trace_tool_output,
    check_price_consistency
)


# ========== 1. 工具参数检查 ==========

def test_tool_args_pass():
    trace = {"tool_args": {"departure": "NRT", "destination": "SHA"}}
    assert check_trace_tool_args(trace) == "Pass"


def test_tool_args_wrong_value():
    # OSA = 大阪，不是东京的三个合法代码之一，应判 Fail
    trace = {"tool_args": {"departure": "OSA", "destination": "SHA"}}
    assert check_trace_tool_args(trace).startswith("Fail")


def test_tool_args_tyo_pass():
    # 真链路模型常报城市码 TYO 而非机场码 NRT/HND，同城等价应判 Pass
    trace = {"tool_args": {"departure": "TYO", "destination": "PVG"}}
    assert check_trace_tool_args(trace) == "Pass"


def test_tool_args_wrong_type():
    trace = {"tool_args": None}
    assert check_trace_tool_args(trace).startswith("Fail")


# ========== 2. 工具名检查 ==========

def test_tool_name_pass():
    trace = {"tool_name": "search_flights"}
    assert check_trace_tool_name(trace) == "Pass"


def test_tool_name_wrong():
    trace = {"tool_name": "book_flight"}
    assert check_trace_tool_name(trace).startswith("Fail")


# ========== 3. 工具返回检查 ==========

def test_tool_output_pass():
    trace = {"tool_output": {"lowest_price": 1200}}
    assert check_trace_tool_output(trace) == "Pass"


def test_tool_output_missing_price():
    trace = {"tool_output": {}}
    assert check_trace_tool_output(trace).startswith("Fail")


# ========== 4. 结果一致性检查 ==========

def test_price_consistency_pass():
    trace = {
        "tool_output": {"lowest_price": 1200},
        "final_output": "最低价格是1200元"
    }
    assert check_price_consistency(trace) == "Pass"


def test_price_consistency_mismatch():
    trace = {
        "tool_output": {"lowest_price": 1200},
        "final_output": "最低价格是1500元"
    }
    assert check_price_consistency(trace).startswith("Fail")


def test_price_consistency_no_price():
    trace = {
        "tool_output": {"lowest_price": 1200},
        "final_output": "已经为您查询了航班信息"
    }
    assert check_price_consistency(trace).startswith("Fail")
