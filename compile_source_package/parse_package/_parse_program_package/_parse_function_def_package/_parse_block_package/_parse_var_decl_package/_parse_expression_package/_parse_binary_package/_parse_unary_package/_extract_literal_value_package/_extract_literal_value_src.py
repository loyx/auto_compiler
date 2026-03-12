# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple extraction logic

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (NUMBER 或 STRING)
#   "value": str,            # token 值 (如 "42", "3.14", "\"hello\"")
#   "line": int,             # 行号
#   "column": int            # 列号
# }

# === main function ===
def _extract_literal_value(token: Token) -> Any:
    """
    将 NUMBER 或 STRING token 的值解析为 Python 字面值。
    
    Args:
        token: token 字典，type 必须是 "NUMBER" 或 "STRING"
    
    Returns:
        NUMBER: 返回 int 或 float
        STRING: 返回去掉引号的字符串
    """
    token_type = token.get("type", "")
    token_value = token.get("value", "")
    
    if token_type == "NUMBER":
        return _parse_number_value(token_value)
    elif token_type == "STRING":
        return _parse_string_value(token_value)
    else:
        return token_value

# === helper functions ===
def _parse_number_value(value: str) -> Any:
    """
    解析数字字符串为 int 或 float。
    
    Args:
        value: 数字字符串 (如 "42", "3.14")
    
    Returns:
        包含 '.' 或科学计数法返回 float，否则返回 int。空字符串返回空字符串。
    """
    if value == "":
        return ""
    # 科学计数法或包含小数点的返回 float
    if "." in value or "e" in value.lower():
        return float(value)
    else:
        return int(value)

def _parse_string_value(value: str) -> str:
    """
    解析字符串字面值，去掉首尾引号。
    
    Args:
        value: 字符串值 (如 "\"hello\"", "'world'")
    
    Returns:
        去掉首尾引号的字符串
    """
    if len(value) >= 2:
        first_char = value[0]
        last_char = value[-1]
        # 检查首尾是否为相同的引号
        if first_char == last_char and first_char in ('"', "'"):
            return value[1:-1]
    return value

# === OOP compatibility layer ===
# Not needed: this is a pure helper function with no framework requirements
