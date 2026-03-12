# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions for this utility function

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
def _consume_token(
    parser_state: ParserState,
    expected_type: str = None,
    expected_value: str = None
) -> Token:
    """
    Consume current token and advance parser position.
    
    Args:
        parser_state: Parser state dictionary containing tokens, current position, and filename
        expected_type: Optional expected token type for validation
        expected_value: Optional expected token value for validation
    
    Returns:
        The consumed token dictionary
    
    Raises:
        SyntaxError: If token doesn't match expectations or end of input is reached
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # Check if we've reached the end of tokens
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input at {filename}")
    
    # Get the current token
    token = tokens[pos]
    line = token.get("line", 0)
    column = token.get("column", 0)
    
    # Validate token type if expected_type is provided
    if expected_type is not None and token["type"] != expected_type:
        raise SyntaxError(
            f"Expected token type '{expected_type}' but got '{token['type']}' "
            f"at {filename}:{line}:{column}"
        )
    
    # Validate token value if expected_value is provided
    if expected_value is not None and token["value"] != expected_value:
        raise SyntaxError(
            f"Expected token value '{expected_value}' but got '{token['value']}' "
            f"at {filename}:{line}:{column}"
        )
    
    # Advance the position
    parser_state["pos"] = pos + 1
    
    return token

# === helper functions ===
# No helper functions needed for this simple token consumption function

# === OOP compatibility layer ===
# Not needed for this utility function
