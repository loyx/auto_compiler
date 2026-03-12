# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple utility

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
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
    Consume a token of the expected type from the parser state.
    
    Args:
        parser_state: Current parser state containing tokens, pos, filename
        expected_type: The expected token type string
        
    Returns:
        The matched Token object
        
    Raises:
        SyntaxError: If current token doesn't match expected_type or pos is out of bounds
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # Check boundary condition
    if pos >= len(tokens):
        raise SyntaxError(
            f"Expected {expected_type} at {filename}:EOF, but found end of input"
        )
    
    # Get current token
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    line = current_token.get("line", 0)
    column = current_token.get("column", 0)
    
    # Validate token type
    if token_type != expected_type:
        raise SyntaxError(
            f"Expected {expected_type} at {filename}:{line}:{column}, but found {token_type}"
        )
    
    # Advance position (in-place modification)
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function