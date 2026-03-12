# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# 此函数不调用任何子函数，无需导入

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
def _peek_token(parser_state: ParserState) -> Token | None:
    """
    Peek at the current token without consuming it.
    
    Args:
        parser_state: Parser state dictionary containing:
            - tokens: List of token dictionaries
            - pos: Current position pointer (integer index)
    
    Returns:
        Token dictionary at current position if exists, otherwise None.
        Does not modify parser_state (no side effects).
    """
    # Extract tokens list and position pointer
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # Check if position is within valid range
    if isinstance(tokens, list) and 0 <= pos < len(tokens):
        return tokens[pos]
    
    # Position out of range or tokens is not a list
    return None

# === helper functions ===
# 此函数逻辑简单，无需辅助函数

# === OOP compatibility layer ===
# 此函数为纯函数，无需 OOP wrapper
# 不生成 class wrapper