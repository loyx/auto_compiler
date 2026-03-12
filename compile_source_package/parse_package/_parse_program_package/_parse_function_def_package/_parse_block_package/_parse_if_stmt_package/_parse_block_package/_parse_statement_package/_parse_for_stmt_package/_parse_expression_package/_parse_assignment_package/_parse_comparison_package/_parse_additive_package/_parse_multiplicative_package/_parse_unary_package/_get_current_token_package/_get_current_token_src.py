# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No sub functions needed - this is a leaf utility function

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
def _get_current_token(parser_state: ParserState) -> Optional[Token]:
    """
    Get the current token from parser state.
    
    Args:
        parser_state: Dictionary containing tokens list and current position
        
    Returns:
        Current token dict if pos is valid, None otherwise
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if 0 <= pos < len(tokens):
        return tokens[pos]
    return None

# === helper functions ===
# No helper functions needed for this simple utility

# === OOP compatibility layer ===
# Not needed - this is a utility function, not a framework entry point
