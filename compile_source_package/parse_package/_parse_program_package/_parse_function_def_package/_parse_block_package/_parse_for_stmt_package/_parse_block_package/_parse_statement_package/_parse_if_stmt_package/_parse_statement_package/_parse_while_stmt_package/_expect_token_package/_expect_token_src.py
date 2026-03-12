# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed for this utility

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
def _expect_token(parser_state: ParserState, token_type: str) -> Token:
    """
    验证并消耗指定类型的 token。
    
    1. 检查 parser_state["pos"] 是否越界，若越界抛出 SyntaxError
    2. 获取当前 token，检查其 type 是否匹配 token_type
    3. 若匹配，消耗该 token（pos += 1），返回该 token
    4. 若不匹配，抛出 SyntaxError，包含期望类型和实际类型信息
    
    副作用：更新 parser_state["pos"]
    异常：SyntaxError 当 token 类型不匹配或已到达 token 末尾
    """
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    
    # 检查是否越界
    if pos >= len(tokens):
        filename = parser_state.get("filename", "<unknown>")
        raise SyntaxError(f"Unexpected end of input in {filename}: expected token type '{token_type}'")
    
    # 获取当前 token
    current_token = tokens[pos]
    
    # 检查 token 类型是否匹配
    if current_token["type"] != token_type:
        filename = parser_state.get("filename", "<unknown>")
        raise SyntaxError(
            f"Syntax error in {filename} at line {current_token.get('line', '?')}, "
            f"column {current_token.get('column', '?')}: "
            f"expected token type '{token_type}', got '{current_token['type']}'"
        )
    
    # 消耗 token（更新 pos）
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
