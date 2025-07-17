TOOL_DESCRIPTIONS = {
    "finance": [
        {"name": "StockTool", "description": "Get real-time stock prices"},
        {"name": "TaxCalc", "description": "Calculate income tax"}
    ],
    "medical": [
        {"name": "DrugInfo", "description": "Get drug interactions"},
        {"name": "SymptomChecker", "description": "Check symptoms"}
    ]
}

def get_tools_for_domain(domain):
    tools = TOOL_DESCRIPTIONS.get(domain, [])
    return "\n".join(f"{t['name']}: {t['description']}" for t in tools)

