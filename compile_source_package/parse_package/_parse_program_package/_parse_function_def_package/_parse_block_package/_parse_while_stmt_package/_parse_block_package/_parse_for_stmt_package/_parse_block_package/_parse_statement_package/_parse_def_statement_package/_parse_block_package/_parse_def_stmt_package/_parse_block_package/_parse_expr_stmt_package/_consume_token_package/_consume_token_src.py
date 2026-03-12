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
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _consume_token(parser_state: ParserState, expected_type: str) -> Token:
    """
    Consume a token of the expected type from the parser state.
    
    Args:
        parser_state: Parser state containing tokens list and current position
        expected_type: The expected token type string
        
    Returns:
        The consumed token
        
    Raises:
        SyntaxError: If no token available or token type doesn't match
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if there are more tokens
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input, expected {expected_type}")
    
    # Get current token
    current_token = tokens[pos]
    actual_type = current_token["type"]
    
    # Check if token type matches
    if actual_type != expected_type:
        raise SyntaxError(f"Expected {expected_type}, got {actual_type}")
    
    # Consume the token by incrementing position
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
