import json
import urllib.request
import urllib.error

# 1. 读取 .env 里的 API Key（简单解析，不依赖 openai 库）
api_key = None
with open(".env", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if line.startswith("DEEPSEEK_API_KEY="):
            api_key = line.split("=", 1)[1].strip().strip('"').strip("'")

if not api_key:
    raise ValueError("没有找到 DEEPSEEK_API_KEY")

# 2. system_prompt（与 deepseek_test.py 保持一致）
system_prompt = """
你是一个机票价格语义识别助手。

你的任务是识别Agent回答中最终确认的最低机票价格。

要求：
1. 理解否定表达和转折表达。
2. 不要简单提取第一个数字。
3. 如果无法确定最低价格，返回null。
4. 必须输出JSON格式。

JSON格式示例：
{
    "lowest_price": 1200,
    "reason": "1200元是最终确认的最低价格"
}
"""

# 3. 只看这三条关键用例
target_ids = ["TC015", "TC017", "TC016"]

with open("test_cases.json", "r", encoding="utf-8") as file:
    test_cases = json.load(file)

for case in test_cases:
    if case["case_id"] not in target_ids:
        continue

    print("用例：", case["case_id"])
    print("输入：", case["final_output"])
    print("我的标注：", case["expected_price"])

    # 4. 用标准库直接调用 DeepSeek 接口（不经过 openai 库）
    payload = {
        "model": "deepseek-flash",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": case["final_output"]}
        ],
        "response_format": {"type": "json_object"},
        "stream": False
    }
    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        data=data,
        headers={
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
        raw = result["choices"][0]["message"]["content"]
        print("模型原始返回：", raw)
    except urllib.error.HTTPError as e:
        print("HTTP错误：", e.code, e.read().decode("utf-8", errors="replace"))
    except Exception as e:
        print("请求失败：", type(e).__name__, e)

    print("----------------------")
