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
#   "tokens": list[Token],
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _expect_token(parser_state: ParserState, token_type: str) -> ParserState:
    """
    Validate and consume the expected token type.
    
    Args:
        parser_state: Current parser state containing tokens list and pos
        token_type: Expected token type (e.g., "RETURN", "SEMICOLON")
    
    Returns:
        Updated parser_state with pos advanced
    
    Raises:
        SyntaxError: If token type doesn't match or pos is out of bounds
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if pos is out of bounds
    if pos >= len(tokens):
        filename = parser_state.get("filename", "unknown")
        raise SyntaxError(
            f"Unexpected end of file in {filename}: expected token type '{token_type}'"
        )
    
    # Get current token
    current_token = tokens[pos]
    
    # Check if token type matches
    if current_token.get("type") != token_type:
        filename = parser_state.get("filename", "unknown")
        line = current_token.get("line", "?")
        column = current_token.get("column", "?")
        actual_type = current_token.get("type", "UNKNOWN")
        raise SyntaxError(
            f"Syntax error in {filename} at line {line}, column {column}: "
            f"expected '{token_type}', got '{actual_type}'"
        )
    
    # Create updated parser state with pos advanced
    updated_state = parser_state.copy()
    updated_state["pos"] = pos + 1
    
    return updated_state

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function