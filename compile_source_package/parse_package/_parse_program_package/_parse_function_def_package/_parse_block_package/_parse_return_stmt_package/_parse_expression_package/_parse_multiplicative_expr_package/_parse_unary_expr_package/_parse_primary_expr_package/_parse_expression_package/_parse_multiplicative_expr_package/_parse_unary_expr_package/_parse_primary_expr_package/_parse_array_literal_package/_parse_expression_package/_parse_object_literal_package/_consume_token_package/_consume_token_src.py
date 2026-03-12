# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions required for this utility function

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
def _consume_token(parser_state: ParserState, expected_type: str) -> Token:
    """
    Consume a token of expected type and advance parser position.
    
    Args:
        parser_state: Parser state dictionary containing tokens and pos
        expected_type: Expected token type string (e.g., "LEFT_BRACE", "COMMA")
    
    Returns:
        The consumed token
    
    Raises:
        ValueError: If pos is out of bounds or token type doesn't match expected_type
    """
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    filename = parser_state.get("filename", "<unknown>")
    
    # Check if pos is out of bounds
    if pos >= len(tokens):
        raise ValueError(
            f"Unexpected end of input: expected token type '{expected_type}' "
            f"but reached end of file at {filename}"
        )
    
    # Get current token
    current_token = tokens[pos]
    
    # Verify token type matches expected type
    if current_token["type"] != expected_type:
        actual_type = current_token["type"]
        line = current_token.get("line", "?")
        column = current_token.get("column", "?")
        raise ValueError(
            f"Syntax error at {filename}:{line}:{column}: "
            f"expected token type '{expected_type}' but got '{actual_type}'"
        )
    
    # Advance position and return token
    parser_state["pos"] = pos + 1
    return current_token

# === helper functions ===
# No helper functions needed for this simple utility

# === OOP compatibility layer ===
# Not required for this helper function
