# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
# No child functions required for this utility function

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
    Return the current token at parser_state["pos"] or None if at end.
    Does not modify parser_state (read-only operation).
    """
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    
    if pos < len(tokens):
        return tokens[pos]
    else:
        return None

# === helper functions ===
# No helper functions needed for this simple utility

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a utility function, not a framework entry point
