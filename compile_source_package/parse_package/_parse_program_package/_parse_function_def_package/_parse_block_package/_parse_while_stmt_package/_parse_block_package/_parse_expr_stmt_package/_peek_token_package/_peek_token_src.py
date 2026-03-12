# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No sub functions needed for this simple peek operation

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
    查看当前位置的 token 但不消费。
    
    输入：parser_state（包含 tokens 列表和 pos 位置）
    输出：当前 token（dict）或 None（如果 pos 已超出 tokens 列表末尾）
    
    不修改 parser_state 的任何字段。
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
