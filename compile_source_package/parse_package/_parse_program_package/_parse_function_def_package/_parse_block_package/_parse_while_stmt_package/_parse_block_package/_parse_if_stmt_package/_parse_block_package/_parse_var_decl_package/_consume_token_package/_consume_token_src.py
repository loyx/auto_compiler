# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed

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
def _consume_token(parser_state: dict, expected_type: str = None) -> dict:
    """
    Consume current token, optionally validate type.
    
    Args:
        parser_state: Parser state dict with tokens list and pos index
        expected_type: Optional expected token type to validate
    
    Returns:
        The consumed token dict
    
    Raises:
        SyntaxError: If pos is out of bounds or token type doesn't match
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check bounds
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input at position {pos}")
    
    # Get current token
    token = tokens[pos]
    
    # Validate type if expected_type is provided
    if expected_type is not None and token["type"] != expected_type:
        raise SyntaxError(
            f"Expected token type '{expected_type}' but got '{token['type']}' "
            f"at line {token.get('line', '?')}, column {token.get('column', '?')}"
        )
    
    # Increment position
    parser_state["pos"] = pos + 1
    
    # Return consumed token
    return token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function
