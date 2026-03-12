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
    检查当前 token 类型是否匹配 expected_type，若匹配则消费（pos+1）并返回更新后的 parser_state；
    若不匹配则抛出 SyntaxError。
    """
    token = _peek_token(parser_state)
    
    if token is None:
        raise SyntaxError("Unexpected end of input")
    
    if token["type"] != expected_type:
        raise SyntaxError(f"Expected {expected_type} but got {token['type']}")
    
    # 创建副本并更新 pos
    new_state = parser_state.copy()
    new_state["pos"] = parser_state["pos"] + 1
    return new_state

# === helper functions ===
# (none needed)

# === OOP compatibility layer ===
# (not needed for this function node)
