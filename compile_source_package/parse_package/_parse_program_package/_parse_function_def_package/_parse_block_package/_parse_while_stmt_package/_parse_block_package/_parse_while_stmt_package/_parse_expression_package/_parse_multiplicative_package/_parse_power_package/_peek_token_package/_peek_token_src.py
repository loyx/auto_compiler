# === std / third-party imports ===
from typing import Any, Dict, Optional

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
#   "error": str
# }

# === main function ===
def _peek_token(parser_state: ParserState) -> Optional[Token]:
    """
    查看当前位置的 token 但不消费（不移动位置指针）。
    
    从 parser_state 中获取 tokens 列表和 pos 位置指针。
    如果 pos 在有效范围内（0 <= pos < len(tokens)），返回 tokens[pos]。
    如果 pos 超出范围（已到达末尾），返回 None。
    不修改 parser_state。
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if 0 <= pos < len(tokens):
        return tokens[pos]
    else:
        return None

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
