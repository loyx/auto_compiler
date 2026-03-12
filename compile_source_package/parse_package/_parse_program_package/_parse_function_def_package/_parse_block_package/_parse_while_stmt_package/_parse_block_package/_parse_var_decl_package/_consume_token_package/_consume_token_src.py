# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions for this module

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _consume_token(parser_state: ParserState, expected_type: str) -> ParserState:
    """
    消费指定类型的 token。
    
    检查当前 token 类型是否匹配期望类型，若匹配则推进位置。
    若不匹配或已到达输入末尾，抛出 SyntaxError。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否超出 token 列表范围
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input, expected {expected_type}")
    
    # 获取当前 token
    current_token = tokens[pos]
    actual_type = current_token["type"]
    
    # 检查类型是否匹配
    if actual_type != expected_type:
        raise SyntaxError(f"Expected {expected_type}, got {actual_type}")
    
    # 创建新的 parser_state，pos + 1
    new_state = parser_state.copy()
    new_state["pos"] = pos + 1
    
    return new_state

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function