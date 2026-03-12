# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this leaf node

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
def _peek_token(parser_state: ParserState) -> Token | None:
    """
    查看 parser_state 当前 pos 位置的 token 而不消费。
    
    不修改 parser_state 的任何内容。
    如果 pos 超出有效范围，返回 None。
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 检查 pos 是否在有效范围内
    if 0 <= pos < len(tokens):
        return tokens[pos]
    
    # 已到达输入末尾
    return None

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
