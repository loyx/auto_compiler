# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this utility function

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }


# === main function ===
def _expect_token(parser_state: ParserState, expected_type: str) -> Token:
    """
    期望当前 token 为指定类型。
    
    如果当前 token 类型匹配 expected_type，则 pos 前进 1 并返回该 token；
    如果不匹配或越界，抛出 SyntaxError。
    """
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    
    # Step 1: Check bounds
    if pos >= len(tokens):
        raise SyntaxError(
            f"Unexpected end of input in {parser_state.get('filename', '<unknown>')}: "
            f"expected {expected_type} but found nothing"
        )
    
    # Step 2: Get current token
    current_token = tokens[pos]
    
    # Step 3 & 4: Check type match
    if current_token["type"] != expected_type:
        raise SyntaxError(
            f"Syntax error in {parser_state.get('filename', '<unknown>')} at line {current_token.get('line', '?')}, column {current_token.get('column', '?')}: "
            f"expected {expected_type} but found {current_token['type']} ('{current_token.get('value', '')}')"
        )
    
    # Step 3: Advance position and return token
    parser_state["pos"] = pos + 1
    return current_token


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function