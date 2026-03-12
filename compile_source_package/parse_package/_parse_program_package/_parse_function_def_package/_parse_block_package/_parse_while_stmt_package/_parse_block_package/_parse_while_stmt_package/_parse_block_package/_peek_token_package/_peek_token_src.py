# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No subfunctions needed for this simple peek operation

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
    Peek at the current token without consuming it.
    
    Args:
        parser_state: Parser state dictionary containing tokens list and pos pointer
        
    Returns:
        Current token dict if available, None if pos is out of bounds
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # Check if pos is within valid range
    if pos < 0 or pos >= len(tokens):
        return None
    
    # Return the token at current position without modifying state
    return tokens[pos]

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a helper function, not a framework entry point
