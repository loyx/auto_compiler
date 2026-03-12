# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No subfunctions needed for this utility function

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
    查看当前 token 但不消费位置。
    
    Args:
        parser_state: 解析器状态字典，包含 tokens、pos、filename 等字段
        
    Returns:
        当前 token 字典（包含 type, value, line, column）或 None（当 pos 超出 tokens 列表范围时）
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos < len(tokens):
        return tokens[pos]
    return None

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function