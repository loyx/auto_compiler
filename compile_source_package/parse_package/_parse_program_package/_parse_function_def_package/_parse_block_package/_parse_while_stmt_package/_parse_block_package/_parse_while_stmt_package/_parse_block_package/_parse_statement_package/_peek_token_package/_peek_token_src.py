# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No sub functions required for this utility

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
    
    Returns the token at parser_state["tokens"][parser_state["pos"]]
    if pos is within valid range, otherwise returns None (EOF).
    Does not modify parser_state.
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos < 0 or pos >= len(tokens):
        return None
    
    return tokens[pos]

# === helper functions ===
# No helper functions needed for this simple utility

# === OOP compatibility layer ===
# Not required - this is a utility function, not a framework entry point
