from batch_checker import check_tool_001


expected_params = {
    "departure": "NRT",
    "destination": "PVG"
}

actual_params = {
    "departure": "PVG",
    "destination": "NRT"
}

if actual_params["departure"] != expected_params["departure"]:
    print("出发地参数错误")

if actual_params["destination"] != expected_params["destination"]:
    print("目的地参数错误")

actual_params = None

result = check_tool_001(actual_params)

print(result)