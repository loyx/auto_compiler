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
    Return the token at the current position in parser_state.
    
    Pure read operation - does not modify parser_state.
    Returns None if pos is out of bounds.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        return None
    
    return tokens[pos]

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
