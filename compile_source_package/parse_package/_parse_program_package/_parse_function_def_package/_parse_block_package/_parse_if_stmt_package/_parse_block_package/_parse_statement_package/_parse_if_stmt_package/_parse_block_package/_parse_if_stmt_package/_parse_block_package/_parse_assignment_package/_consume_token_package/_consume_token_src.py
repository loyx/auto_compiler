# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this helper

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
def _consume_token(parser_state: ParserState, expected_type: str) -> Token:
    """
    Consume current token from parser state and validate its type.
    
    Args:
        parser_state: Parser state containing tokens list and current pos
        expected_type: Expected token type string (e.g., "IDENT", "ASSIGN")
    
    Returns:
        The consumed token dict
    
    Side effects:
        Modifies parser_state["pos"] on success
        May set parser_state["error"] on failure
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if pos is out of bounds
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input"
        return {}
    
    # Get current token
    token = tokens[pos]
    
    # Check if token type matches expected type
    if token["type"] == expected_type:
        # Match: increment pos and return token
        parser_state["pos"] = pos + 1
        return token
    else:
        # Mismatch: set error and return token
        parser_state["error"] = f"Expected {expected_type}, got {token['type']}"
        return token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function
