# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No child functions needed for this simple accessor

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
def _current_token(parser_state: ParserState) -> Optional[Token]:
    """
    获取解析器当前位置的 token。
    
    从 parser_state 中读取 tokens 列表和 pos 位置，
    如果 pos 在有效范围内则返回对应 token，否则返回 None。
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if 0 <= pos < len(tokens):
        return tokens[pos]
    return None

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function