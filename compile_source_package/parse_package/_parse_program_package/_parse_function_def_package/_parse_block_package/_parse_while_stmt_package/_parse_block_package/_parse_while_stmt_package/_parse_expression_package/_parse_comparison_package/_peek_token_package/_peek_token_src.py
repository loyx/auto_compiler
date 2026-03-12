# === std / third-party imports ===
from typing import Any, Dict

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
def _peek_token(parser_state: ParserState) -> Token:
    """
    Look at current token without consuming it.
    
    Returns the token at current position if available, None otherwise.
    Does not modify parser_state.
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos < 0 or pos >= len(tokens):
        return None
    
    return tokens[pos]

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
