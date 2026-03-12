# === std / third-party imports ===
from typing import Any, Dict

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
def _consume_token(parser_state: ParserState, expected_type: str) -> ParserState:
    """
    Consume current token if it matches expected type.
    
    Args:
        parser_state: Parser state containing tokens list and current position
        expected_type: Expected token type string (e.g., "IDENTIFIER", "PLUS")
    
    Returns:
        Updated parser_state with pos advanced by 1
    
    Raises:
        SyntaxError: If pos is out of bounds or token type doesn't match
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if pos is within bounds
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    # Get current token
    token = tokens[pos]
    
    # Check if token type matches expected type
    if token["type"] != expected_type:
        raise SyntaxError(f"Expected {expected_type}, got {token['type']}")
    
    # Create new parser_state with pos advanced
    new_parser_state = {
        "tokens": tokens,
        "pos": pos + 1,
        "filename": parser_state.get("filename", ""),
        "error": parser_state.get("error", "")
    }
    
    return new_parser_state

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function