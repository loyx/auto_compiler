# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No sub functions needed for this simple mapping logic

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (如 STAR, PLUS, AND 等)
#   "value": str,            # token 值 (如 "*", "+", "and" 等)
#   "line": int,             # 行号
#   "column": int            # 列号
# }

OperatorPrecedence = Tuple[int, str]
# OperatorPrecedence possible fields:
# {
#   "precedence": int,       # 运算符优先级 (0-4, -1 表示非运算符)
#   "associativity": str     # 结合性 ("left" 或 "right")
# }

# === main function ===
def _get_operator_precedence(token: Token) -> OperatorPrecedence:
    """
    根据 token 的 type 字段返回运算符的优先级和结合性。
    
    运算符优先级表：
    - STAR_STAR: 4, right
    - STAR, SLASH, PERCENT: 3, left
    - PLUS, MINUS: 2, left
    - EQUAL_EQUAL, BANG_EQUAL, LESS, GREATER, LESS_EQUAL, GREATER_EQUAL: 1, left
    - AND, OR: 0, left
    - 非运算符: -1, left
    """
    token_type = token.get("type", "")
    
    # Priority 4: right associative
    if token_type == "STAR_STAR":
        return (4, "right")
    
    # Priority 3: left associative
    if token_type in ("STAR", "SLASH", "PERCENT"):
        return (3, "left")
    
    # Priority 2: left associative
    if token_type in ("PLUS", "MINUS"):
        return (2, "left")
    
    # Priority 1: left associative
    if token_type in ("EQUAL_EQUAL", "BANG_EQUAL", "LESS", "GREATER", "LESS_EQUAL", "GREATER_EQUAL"):
        return (1, "left")
    
    # Priority 0: left associative
    if token_type in ("AND", "OR"):
        return (0, "left")
    
    # Not an operator
    return (-1, "left")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function