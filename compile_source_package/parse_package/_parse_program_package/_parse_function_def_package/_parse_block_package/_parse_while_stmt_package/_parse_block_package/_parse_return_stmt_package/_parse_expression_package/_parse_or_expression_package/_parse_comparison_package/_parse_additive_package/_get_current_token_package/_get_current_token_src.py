# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No sub functions needed for this simple helper

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
    Get the token at the current position in parser state.
    
    Args:
        parser_state: Parser state dictionary containing tokens list and pos
        
    Returns:
        Token dict if pos is within valid range, None otherwise
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if 0 <= pos < len(tokens):
        return tokens[pos]
    return None

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function