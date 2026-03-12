# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===

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
    查看当前 token 但不消费。
    
    输入：parser_state - 解析器状态字典
    输出：当前 token 字典，如果已到达 token 末尾则返回 None
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos < 0 or pos >= len(tokens):
        return None
    
    return tokens[pos]

# === helper functions ===

# === OOP compatibility layer ===
