# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._peek_token_package._peek_token_src import _peek_token

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
def _consume_token(parser_state: dict, expected_type: str) -> dict:
    """
    消费期望类型的 token。
    
    输入：parser_state 解析器状态，expected_type 期望的 token 类型
    输出：更新后的 parser_state（pos 已推进 1）
    如果 token 类型不匹配或到达文件末尾，抛出 SyntaxError
    """
    token = _peek_token(parser_state)
    
    if token is None:
        raise SyntaxError(f"Unexpected end of file, expected '{expected_type}'")
    
    token_type = token.get("type")
    line = token.get("line", 0)
    
    if token_type != expected_type:
        raise SyntaxError(f"Expected token '{expected_type}', got '{token_type}' at line {line}")
    
    new_state = dict(parser_state)
    new_state["pos"] = parser_state["pos"] + 1
    return new_state

# === helper functions ===

# === OOP compatibility layer ===
