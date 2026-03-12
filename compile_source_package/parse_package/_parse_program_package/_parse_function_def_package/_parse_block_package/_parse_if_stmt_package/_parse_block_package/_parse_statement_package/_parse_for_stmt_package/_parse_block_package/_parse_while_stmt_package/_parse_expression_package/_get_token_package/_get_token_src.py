# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No child functions

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
def _get_token(parser_state: ParserState) -> Optional[Token]:
    """获取当前位置的 token。
    
    从 parser_state 中读取 tokens 列表和 pos 位置，
    返回当前位置的 token，如果越界则返回 None。
    无副作用：不修改 parser_state 的任何字段。
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens):
        return None
    
    return tokens[pos]

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
