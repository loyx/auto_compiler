# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple token consumption logic

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
def _consume_token(parser_state: dict, expected_type: str = None, expected_value: str = None) -> dict:
    """
    Consume current token and advance position.
    
    Args:
        parser_state: Parser state dict containing tokens, pos, filename
        expected_type: Optional expected token type to validate against
        expected_value: Optional expected token value to validate against
    
    Returns:
        The consumed token dict
    
    Raises:
        SyntaxError: If end of input or token doesn't match expectations
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check for end of input
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    # Get current token
    current_token = tokens[pos]
    
    # Validate against expected_type if provided
    if expected_type is not None and current_token.get("type") != expected_type:
        actual_type = current_token.get("type", "<unknown>")
        raise SyntaxError(f"Expected token type '{expected_type}', got '{actual_type}'")
    
    # Validate against expected_value if provided
    if expected_value is not None and current_token.get("value") != expected_value:
        actual_value = current_token.get("value", "<unknown>")
        raise SyntaxError(f"Expected token value '{expected_value}', got '{actual_value}'")
    
    # Advance position
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# No helper functions needed - logic is simple and self-contained

# === OOP compatibility layer ===
# Not needed - this is a parser utility function, not a framework entry point
