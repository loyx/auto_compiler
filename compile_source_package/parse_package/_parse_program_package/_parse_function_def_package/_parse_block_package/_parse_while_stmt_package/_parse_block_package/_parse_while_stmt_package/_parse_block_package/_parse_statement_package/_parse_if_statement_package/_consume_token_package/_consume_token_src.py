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

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }


# === main function ===
def _consume_token(parser_state: ParserState, expected_type: str = None) -> Token:
    """
    Consumes current token from parser_state and advances pos in-place.
    
    Args:
        parser_state: Parser state dict containing tokens list and pos index
        expected_type: Optional expected token type for validation
    
    Returns:
        The consumed token dict
    
    Raises:
        SyntaxError: If pos is at EOF or token type doesn't match expected_type
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check for EOF
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input at {parser_state.get('filename', 'unknown')}")
    
    current_token = tokens[pos]
    
    # Validate token type if expected_type is provided
    if expected_type is not None and current_token["type"] != expected_type:
        raise SyntaxError(
            f"Expected token type '{expected_type}', got '{current_token['type']}' "
            f"at line {current_token.get('line', '?')}, column {current_token.get('column', '?')}"
        )
    
    # Advance position (in-place modification)
    parser_state["pos"] = pos + 1
    
    return current_token


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed - this is a utility function, not a framework entry point
