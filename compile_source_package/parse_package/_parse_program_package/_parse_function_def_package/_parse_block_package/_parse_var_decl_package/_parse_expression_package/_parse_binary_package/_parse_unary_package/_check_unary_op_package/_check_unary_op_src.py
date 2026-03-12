# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (MINUS, PLUS, NOT, TILDE, etc.)
#   "value": str,            # token 值 (如 "-", "+", "!", "not", "~", etc.)
#   "line": int,             # 行号
#   "column": int            # 列号
# }

# === main function ===
def _check_unary_op(token: dict) -> bool:
    """
    判断 token 是否为一元运算符。
    
    一元运算符包括：
    - MINUS: 对应 "-"
    - PLUS: 对应 "+"
    - TILDE: 对应 "~"
    - NOT: 对应 "!" 或 "not" 关键字
    
    Args:
        token: token 字典，可能为 None（如果越界）
    
    Returns:
        True: 是一元运算符
        False: 不是
    """
    if token is None:
        return False
    
    unary_types = {"MINUS", "PLUS", "TILDE", "NOT"}
    return token.get("type") in unary_types

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this utility function
