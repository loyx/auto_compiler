# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No subfunctions needed

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
def _consume_token(parser_state: ParserState, expected_type: str) -> Tuple[Token, ParserState]:
    """
    Consume current token if it matches expected_type.
    
    Returns (Token, ParserState) where Token is the consumed token and
    ParserState is the updated state with pos advanced.
    Sets error in ParserState if token type doesn't match or end of input.
    Follows immutable pattern: does not modify input parser_state.
    """
    # Create a copy to maintain immutability
    new_state = parser_state.copy()
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # Check if pos is within tokens range
    if pos >= len(tokens):
        new_state["error"] = "Unexpected end of input"
        return (None, new_state)
    
    # Get current token
    current_token = tokens[pos]
    current_token_type = current_token.get("type")
    
    # Check if token type matches expected_type
    if current_token_type != expected_type:
        new_state["error"] = f"Expected {expected_type}, got {current_token_type}"
        return (None, new_state)
    
    # Token matches - advance pos and return
    new_state["pos"] = pos + 1
    return (current_token, new_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
