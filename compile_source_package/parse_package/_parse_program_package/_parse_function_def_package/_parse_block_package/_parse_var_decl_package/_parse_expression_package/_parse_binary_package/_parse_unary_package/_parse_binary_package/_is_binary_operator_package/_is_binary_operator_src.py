# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (如 STAR, PLUS, AND 等)
#   "value": str,            # token 值 (如 "*", "+", "and" 等)
#   "line": int,             # 行号
#   "column": int            # 列号
# }

# === main function ===
def _is_binary_operator(token: Token) -> bool:
    """
    判断给定的 token 是否为二元运算符。
    
    二元运算符 Token Type 列表：
    - STAR_STAR (**)
    - STAR, SLASH, PERCENT (*, /, %)
    - PLUS, MINUS (+, -)
    - EQUAL_EQUAL, BANG_EQUAL, LESS, GREATER, LESS_EQUAL, GREATER_EQUAL (==, !=, <, >, <=, >=)
    - AND, OR
    
    返回值：
    - 如果 token 是上述类型之一，返回 True
    - 如果 token 是 None 或其他类型，返回 False
    
    无副作用，纯函数。
    """
    if token is None:
        return False
    
    binary_operator_types = {
        "STAR_STAR",
        "STAR",
        "SLASH",
        "PERCENT",
        "PLUS",
        "MINUS",
        "EQUAL_EQUAL",
        "BANG_EQUAL",
        "LESS",
        "GREATER",
        "LESS_EQUAL",
        "GREATER_EQUAL",
        "AND",
        "OR",
    }
    
    token_type = token.get("type")
    return token_type in binary_operator_types

# === helper functions ===

# === OOP compatibility layer ===
