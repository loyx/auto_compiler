# === std / third-party imports ===
from typing import Any, Dict

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
def _peek_token(parser_state: ParserState) -> Token | None:
    """
    Returns current token at parser_state pos without modifying state.
    
    Args:
        parser_state: Parser state dictionary containing tokens list and pos index
        
    Returns:
        Token dictionary if not at EOF, None otherwise
        
    Behavior:
        1. If parser_state["pos"] < len(parser_state["tokens"]), return the token at that position
        2. If at EOF (pos >= len(tokens)), return None
        3. Does not modify parser_state
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
