# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed

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
def _is_binary_operator(token: Token) -> bool:
    """
    判断给定 token 是否为二元运算符。
    
    支持的二元运算符：
    - 逻辑运算：AND、OR
    - 比较运算：==、!=、<、>、<=、>=
    - 算术运算：+、-、*、/
    
    无副作用，纯函数。
    """
    BINARY_OPERATORS = {"==", "!=", "<", ">", "<=", ">=", "+", "-", "*", "/"}
    
    token_type = token.get("type")
    token_value = token.get("value")
    
    # 检查是否为关键字 AND 或 OR
    if token_type == "KEYWORD" and token_value in {"AND", "OR"}:
        return True
    
    # 检查是否为运算符符号
    if token_value in BINARY_OPERATORS:
        return True
    
    return False

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this utility function
