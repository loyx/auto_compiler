# === std / third-party imports ===
from typing import Any, Dict, Optional

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
def _consume_token(parser_state: ParserState, expected_type: str) -> Optional[Token]:
    """
    Consume a token of the expected type from the parser state.
    
    If the current token matches expected_type: increment pos and return the token.
    If not matching: record error and return current token without incrementing pos.
    If pos is out of bounds: record error and return None.
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # Check if pos is out of bounds
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input"
        return None
    
    current_token = tokens[pos]
    actual_type = current_token.get("type", "")
    
    # Check if token type matches expected type
    if actual_type == expected_type:
        parser_state["pos"] = pos + 1
        return current_token
    else:
        parser_state["error"] = f"Expected {expected_type} but got {actual_type}"
        return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
