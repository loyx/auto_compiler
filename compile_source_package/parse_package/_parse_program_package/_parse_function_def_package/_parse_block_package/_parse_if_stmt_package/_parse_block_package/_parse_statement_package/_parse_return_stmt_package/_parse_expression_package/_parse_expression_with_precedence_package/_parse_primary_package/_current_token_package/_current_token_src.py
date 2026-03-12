# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No sub functions needed for this simple utility

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
def _current_token(parser_state: ParserState) -> Optional[Token]:
    """获取当前位置的 token。
    
    从 parser_state 中提取 tokens 列表和 pos 位置。
    如果 pos 越界（<0 或 >= len(tokens)），返回 None。
    否则返回 tokens[pos]。
    无副作用。
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos < 0 or pos >= len(tokens):
        return None
    
    return tokens[pos]

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function