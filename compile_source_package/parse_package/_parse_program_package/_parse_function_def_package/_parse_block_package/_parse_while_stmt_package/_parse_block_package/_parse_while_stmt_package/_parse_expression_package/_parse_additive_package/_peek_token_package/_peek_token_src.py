# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No child functions needed for this utility function

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
    
    Reads the token at parser_state["pos"] from parser_state["tokens"].
    Returns None if pos >= len(tokens) (end of token stream).
    Does not modify parser_state["pos"].
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens):
        return None
    
    return tokens[pos]

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
