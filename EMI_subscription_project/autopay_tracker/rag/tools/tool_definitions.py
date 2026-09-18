from rag.tools.db_tools import (
    get_subscriptions,
    get_subscription_by_id,
    get_emis,
    get_emi_by_id,
    get_payment_history,
    get_payment_history_by_id,
    get_categories,
    get_payment_methods,
)

tool_definitions = [
    {
        "type": "function",
        "function": {
            "name": "get_subscriptions",
            "description": "Fetch the current user's list of subscriptions, including name, amount, billing cycle, next due date, status, and auto-renew setting.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_subscription_by_id",
            "description": "Fetch a single subscription belonging to the current user, using its exact ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "subscription_id": {
                        "type": "integer",
                        "description": "The exact ID of the subscription to fetch."
                    }
                },
                "required": ["subscription_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_emis",
            "description": "Fetch the current user's list of EMIs, including item name, total amount, monthly installment, installments paid/remaining, next due date, and status.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_emi_by_id",
            "description": "Fetch a single EMI belonging to the current user, using its exact ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "emi_id": {
                        "type": "integer",
                        "description": "The exact ID of the EMI to fetch."
                    }
                },
                "required": ["emi_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_payment_history",
            "description": "Fetch the current user's payment history, including amount paid, date paid, status, and which subscription or EMI each payment was for.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_payment_history_by_id",
            "description": "Fetch a single payment history record belonging to the current user, using its exact ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "payhistory_id": {
                        "type": "integer",
                        "description": "The exact ID of the payment history record to fetch."
                    }
                },
                "required": ["payhistory_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_categories",
            "description": "Fetch the list of all available categories (such as OTT, Music, Vehicle, Electronics) used to classify subscriptions and EMIs. Categories are shared across all users, not user-specific.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_payment_methods",
            "description": "Fetch the current user's list of payment methods, including type, provider name, and whether it is set as default.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
]

tool_function_map = {
    "get_subscriptions": get_subscriptions,
    "get_subscription_by_id": get_subscription_by_id,
    "get_emis": get_emis,
    "get_emi_by_id": get_emi_by_id,
    "get_payment_history": get_payment_history,
    "get_payment_history_by_id": get_payment_history_by_id,
    "get_categories": get_categories,
    "get_payment_methods": get_payment_methods,
}