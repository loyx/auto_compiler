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
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str | None
# }

# === main function ===
def _peek_token(parser_state: ParserState, offset: int = 0) -> Token | None:
    """
    查看 parser_state 中指定偏移位置的 token，不修改 pos。
    
    行为：
    1. 计算目标位置：target_pos = parser_state['pos'] + offset
    2. 若 target_pos 超出 tokens 范围（< 0 或 >= len(tokens)），返回 None
    3. 返回 tokens[target_pos]
    
    注意：此函数不抛出异常，超出范围返回 None
    """
    tokens = parser_state['tokens']
    current_pos = parser_state['pos']
    target_pos = current_pos + offset
    
    # Check bounds
    if target_pos < 0 or target_pos >= len(tokens):
        return None
    
    return tokens[target_pos]

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
