# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple token consumption logic

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
#   "error": str | None
# }


# === main function ===
def _consume_token(parser_state: ParserState, expected_type: str) -> Token:
    """
    Consume a token of expected type from parser state.
    
    Args:
        parser_state: Parser state containing tokens list and current position
        expected_type: The expected token type string
        
    Returns:
        The consumed token dict
        
    Raises:
        SyntaxError: If no token available or type mismatch
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if pos is within valid range
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    # Get current token
    current_token = tokens[pos]
    actual_type = current_token["type"]
    
    # Check type match
    if actual_type != expected_type:
        line = current_token["line"]
        column = current_token["column"]
        raise SyntaxError(
            f"Expected {expected_type} but got {actual_type} at line {line}, column {column}"
        )
    
    # Advance position (side effect: modify parser_state in place)
    parser_state["pos"] = pos + 1
    
    return current_token


# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# Not needed - this is a simple helper function, not a framework entry point
