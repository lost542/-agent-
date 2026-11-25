# tool_loop_demo.py（第二步：两轮循环 + Trace 记录）
import json
import urllib.request
import urllib.error

def load_api_key():
    with open(".env", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line.startswith("DEEPSEEK_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise ValueError("没有找到 DEEPSEEK_API_KEY")

API_KEY = load_api_key()

TOOLS = [{
    "type": "function",
    "function": {
        "name": "search_flights",
        "description": "查询航班，返回最低价。用户提供出发地和目的地城市代码。",
        "parameters": {
            "type": "object",
            "properties": {
                "departure": {"type": "string", "description": "出发地代码，如 NRT"},
                "destination": {"type": "string", "description": "目的地代码，如 SHA"}
            },
            "required": ["departure", "destination"]
        }
    }
}]

def call_api(messages):
    """发一次请求，返回模型的 message"""
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "tools": TOOLS,
        "tool_choice": "auto",
        "stream": False
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        data=data,
        headers={
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        result = json.loads(response.read().decode("utf-8"))
        return result["choices"][0]["message"]

def search_flights(departure, destination):
    """模拟工具：暂时写死返回，先把循环跑通"""
    return {"lowest_price": 1200, "flights": [{"no": "MU001"}]}

# ===== 主流程 =====
messages = [
    {"role": "system", "content": "你是机票客服。查航班时必须调用 search_flights 工具，不要凭空报价格。"},
    {"role": "user", "content": "帮我查一下东京到上海最低价的航班"}
]

# 第一轮：模型决定调用工具
msg1 = call_api(messages)
tool_call = msg1["tool_calls"][0]
args = json.loads(tool_call["function"]["arguments"])   # 注意 json.loads：arguments 是字符串

# 执行工具
tool_result = search_flights(args["departure"], args["destination"])

# 记 Trace（这就是过程评测要的字段）
trace = {
    "tool_name": tool_call["function"]["name"],
    "tool_args": args,
    "tool_output": tool_result
}
print("工具名:", trace["tool_name"])
print("参数:", trace["tool_args"])
print("工具返回:", trace["tool_output"])

# 第二轮：把工具结果喂回模型，拿最终回答
messages.append(msg1)                                    # ① 原样放回 assistant 的 tool_calls 消息
messages.append({                                        # ② tool 结果消息
    "role": "tool",
    "tool_call_id": tool_call["id"],
    "content": json.dumps(tool_result, ensure_ascii=False)
})
msg2 = call_api(messages)
trace["final_output"] = msg2.get("content")
print("最终回答:", trace["final_output"])
print("完整 Trace:", trace)

# ===== 用真实链路产生的 Trace 喂给 Checker 判定 =====
# 这一步是质变点：过程评测不再跑 mock 手写假数据，而是跑真实 Agent 的轨迹
from trace_checker import check_price_consistency

print("价格一致性判定:", check_price_consistency(trace))
