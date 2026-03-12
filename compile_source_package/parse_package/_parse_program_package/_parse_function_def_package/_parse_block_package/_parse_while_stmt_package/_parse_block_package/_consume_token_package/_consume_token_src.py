# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this utility function

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
#   "tokens": list[Token],
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _consume_token(parser_state: ParserState, expected_type: str) -> ParserState:
    """
    消费期望类型的 token。
    
    输入：parser_state 和 expected_type
    输出：更新后的 parser_state（pos 向前移动一位）
    
    解析规则：
    1. 获取当前 token
    2. 如果当前 token 类型与 expected_type 匹配，则 pos 加 1 并返回更新后的 parser_state
    3. 如果不匹配，抛出 SyntaxError
    
    错误处理：token 类型不匹配或已到达 token 末尾时抛出 SyntaxError。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 检查是否已到达 token 末尾
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of file in {filename}: expected token type '{expected_type}'")
    
    # 获取当前 token
    current_token = tokens[pos]
    current_type = current_token.get("type")
    
    # 检查 token 类型是否匹配
    if current_type != expected_type:
        line = current_token.get("line", "?")
        column = current_token.get("column", "?")
        raise SyntaxError(
            f"Syntax error in {filename} at line {line}, column {column}: "
            f"expected token type '{expected_type}', got '{current_type}'"
        )
    
    # 创建更新后的 parser_state 副本
    updated_state = parser_state.copy()
    updated_state["pos"] = pos + 1
    
    return updated_state

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
