import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from openai import AuthenticationError, APIConnectionError, APITimeoutError
# 1. 读取.env文件
load_dotenv()

# 2. 获取API Key
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError("没有找到DeepSeek API Key，请检查.env文件")

# 3. 创建DeepSeek客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 4. 发送请求

# 1. 设计语义识别任务
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
final_output = "1500元是原价，优惠后最低价格为1200元。"
# 2. 向DeepSeek发送请求
def extract_lowest_price(final_output):

    try:
        response = client.chat.completions.create(
            model="deepseek-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": final_output}
            ],
            response_format={"type": "json_object"},
            stream=False
        )

        result = response.choices[0].message.content
        data = json.loads(result)

        return {
            "status": "SUCCESS",
            "price": data["lowest_price"],
            "error": None
        }


    except json.JSONDecodeError as e:

        return {

            "status": "ERROR",

            "price": None,

            "error": str(e)

        }


    except KeyError as e:

        print("JSON字段缺失：", e)

        return {

            "status": "ERROR",

            "price": None,

            "error": str(e)

        }

    except AuthenticationError as e:
        print("API认证失败：", e)
        return {

            "status": "ERROR",

            "price": None,

            "error": str(e)

        }


    except APIConnectionError as e:

        return {

            "status": "ERROR",

            "price": None,

            "error": str(e)

        }

    except APITimeoutError as e:
        print("API请求超时：", e)
        return {

            "status": "ERROR",

            "price": None,

            "error": str(e)

        }

    except Exception as e:

        print("其他异常：", e)

        return {

            "status": "ERROR",

            "price": None,

            "error": str(e)

        }
# result = '{"price": 1200, "reason": "最低价格是1200元"}'
#
# try:
#     data = json.loads(result)
#     price = data["lowest_price"]
#     print("识别价格：", price)
#
# except json.JSONDecodeError as e:
#     print("JSON解析异常：", e)
#
# except KeyError as e:
#     print("JSON字段缺失：", e)
# result = extract_lowest_price("最低价格不是1500元，而是1200元")
#
# print("完整结果：", result)
# print("运行状态：", result["status"])
# print("识别价格：", result["price"])
# print("错误原因：", result["error"])