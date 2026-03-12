# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .._peek_token_package._peek_token_src import _peek_token

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
    """Consume a token of expected type from parser state."""
    token = _peek_token(parser_state)
    
    if token is None:
        raise SyntaxError("Unexpected end of input")
    
    if token["type"] != expected_type:
        raise SyntaxError(f"Expected {expected_type}, got {token['type']}")
    
    updated_state = parser_state.copy()
    updated_state["pos"] = parser_state["pos"] + 1
    
    return (token, updated_state)

# === helper functions ===

# === OOP compatibility layer ===
