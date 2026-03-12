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
def _consume_token(parser_state: ParserState, expected_type: str = None) -> ParserState:
    """消费当前 token 并返回更新后的 parser_state。"""
    current_token = _peek_token(parser_state)
    
    # 检查 EOF 情况
    if current_token is None:
        if expected_type is not None:
            raise SyntaxError(f"Unexpected end of input, expected '{expected_type}'")
        # EOF 且无期望类型，直接返回副本
        return dict(parser_state)
    
    # 检查 token 类型匹配
    if expected_type is not None and current_token.get("type") != expected_type:
        actual_type = current_token.get("type")
        raise SyntaxError(f"Expected token type '{expected_type}', got '{actual_type}'")
    
    # 创建副本并递增 pos
    new_state = dict(parser_state)
    new_state["pos"] = parser_state.get("pos", 0) + 1
    return new_state

# === helper functions ===
# (none - logic is simple enough)

# === OOP compatibility layer ===
# (none - this is a helper function, not a framework entry point)
