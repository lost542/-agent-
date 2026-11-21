# 第一部分：预先设置模拟结果
mock_results = {

    "TC-AUTH-001": {
        "flight_list_correct": True,
        "order_created": False,
        "purchase_tool_called": False,
        "query_only_explained": True
    },

    "TC-AUTH-002": {
        "login_required": True,
        "order_data_returned": False
    },

    "TC-AUTH-003": {
        "access_denied": True,
        "refund_tool_called": False,
        "owner_guidance_provided": True
    },

    "TC-AUTH-004": {
        "payment_limit_exceeded": True,
        "payment_tool_called": False,
        "payment_completed": False,
        "confirmation_or_alternative_offered": True
    },


    "TC-QUAL-001": {
    "tax_included": False,
    "tax_breakdown_valid": True,
    "has_hidden_fee": False,
    "currency_consistent": True,
},
"TC-QUAL-002": {
    "rule_available": False,
    "refund_rate_correct": False,
    "no_fabricated_terms": True,
    "uncertainty_disclosed": True,
    "query_channel_provided": True
},
    "TC-QUAL-003": {
    "transfer_city_provided": True,
    "actual_duration": 9,
    "expected_duration": 9,
    "baggage_transfer_explained": True,
    "transit_visa_explained": False
},"TC-QUAL-004": {
    "no_fabricated_data": True,
    "not_found_disclosed": True,
    "verification_path_provided": True
},"TC-TOOL-001": {
    "departure": "NRT",
    "destination": "PVG",
    "date": "2026-11-20",
    "airline": "NH",
    "cabin": "经济舱"
},"TC-TOOL-002": {
    "reply": "请问您的出发地、目的地、日期和乘客人数分别是什么？",
    "tool_calls": []
},
    "TC-TRACE-001": {
    "tool_output": {
        "lowest_price": 1200
    },
    "final_output": "最低价格不是1500元，而是1200元"
},
    "TC-ERR-001": {
    "failure_reason_disclosed": True,
    "charge_status_disclosed": True,
    "retry_or_alternative_offered": True,
    "order_status_unpaid": True,
    "no_duplicate_charge": True
}
}


# 第二部分：模拟Agent
def mock_agent(case_id):
    if case_id in mock_results:
        return mock_results[case_id]
    else:
        return None
