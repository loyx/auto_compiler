# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this utility function

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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _consume_token(parser_state: ParserState, token_type: str) -> bool:
    """
    Consume a token of the specified type from the parser state.
    
    Check if parser_state["tokens"][parser_state["pos"]].type equals token_type.
    - If match: increment pos by 1, return True
    - If no match or pos out of bounds: keep pos unchanged, return False
    
    Does not set error or modify other state. Pure utility function.
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # Check bounds
    if pos >= len(tokens):
        return False
    
    # Check token type
    current_token = tokens[pos]
    if current_token.get("type") == token_type:
        parser_state["pos"] = pos + 1
        return True
    
    return False

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function