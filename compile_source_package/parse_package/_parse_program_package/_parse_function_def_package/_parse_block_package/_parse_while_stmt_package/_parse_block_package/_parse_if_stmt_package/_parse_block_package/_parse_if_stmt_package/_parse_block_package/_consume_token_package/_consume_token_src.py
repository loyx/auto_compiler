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

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _consume_token(parser_state: ParserState, expected_type: str) -> Token:
    """
    消耗指定类型的 token 并返回该 token。
    
    处理逻辑：
    1. 获取当前 pos 位置的 token
    2. 检查 token 类型是否匹配 expected_type
    3. 若匹配，parser_state["pos"]++ 并返回该 token
    4. 若不匹配，抛出 SyntaxError
    
    副作用：原地修改 parser_state["pos"]
    异常：类型不匹配或 pos 超出范围时抛出 SyntaxError
    """
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    
    # 检查是否超出 tokens 范围
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    current_token = tokens[pos]
    actual_type = current_token["type"]
    
    # 检查类型是否匹配
    if actual_type != expected_type:
        raise SyntaxError(
            f"Expected token type '{expected_type}', got '{actual_type}' "
            f"at line {current_token.get('line', '?')}, column {current_token.get('column', '?')}"
        )
    
    # 原地递增 pos
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
