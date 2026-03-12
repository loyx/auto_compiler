# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No subfunctions required for this utility function

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
    Peek at current token without consuming it.
    
    Args:
        parser_state: Parser state dictionary containing tokens list and pos pointer
        
    Returns:
        The current token dict if pos is within valid range, None if at end
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos < len(tokens):
        return tokens[pos]
    return None

# === helper functions ===
# No helper functions needed for this simple utility

# === OOP compatibility layer ===
# Not required - this is a utility function, not a framework entry point
