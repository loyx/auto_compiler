# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple lookup operation

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int
# }

# === main function ===
def _get_precedence(token_type: str) -> int:
    """
    获取运算符的优先级数值。
    
    根据 token_type 返回对应的优先级数值，数值越大优先级越高。
    非运算符返回 0。
    
    Args:
        token_type: 运算符的类型字符串（如 "PLUS", "MINUS", "STAR" 等）
    
    Returns:
        int: 优先级值
    """
    precedence_table = {
        # 乘法类：优先级 5
        "STAR": 5,
        "SLASH": 5,
        "PERCENT": 5,
        # 加法类：优先级 4
        "PLUS": 4,
        "MINUS": 4,
        # 比较类：优先级 3
        "LESS": 3,
        "GREATER": 3,
        "LESS_EQUAL": 3,
        "GREATER_EQUAL": 3,
        # 相等类：优先级 2
        "EQUAL_EQUAL": 2,
        "NOT_EQUAL": 2,
        # 逻辑与：优先级 1
        "AND": 1,
        # 逻辑或：优先级 0
        "OR": 0,
    }
    
    return precedence_table.get(token_type, 0)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
