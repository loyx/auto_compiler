# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this utility function

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
def _get_operator_precedence(token: Token) -> int:
    """
    获取二元运算符的优先级数值。
    
    优先级规则（数值越高优先级越高）：
    - 优先级 1：AND、OR（逻辑运算）
    - 优先级 2：==、!=、<、>、<=、>=（比较运算）
    - 优先级 3：+、-（加减运算）
    - 优先级 4：*、/（乘除运算）
    
    Args:
        token: Token 字典，包含 type 和 value 字段，必须是已确认的二元运算符
        
    Returns:
        int: 优先级数值，无效运算符返回 0
    """
    operator = token.get("value", "")
    
    # 优先级 1：逻辑运算
    if operator.upper() in ("AND", "OR"):
        return 1
    
    # 优先级 2：比较运算
    if operator in ("==", "!=", "<", ">", "<=", ">="):
        return 2
    
    # 优先级 3：加减运算
    if operator in ("+", "-"):
        return 3
    
    # 优先级 4：乘除运算
    if operator in ("*", "/"):
        return 4
    
    # 无效运算符
    return 0

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
