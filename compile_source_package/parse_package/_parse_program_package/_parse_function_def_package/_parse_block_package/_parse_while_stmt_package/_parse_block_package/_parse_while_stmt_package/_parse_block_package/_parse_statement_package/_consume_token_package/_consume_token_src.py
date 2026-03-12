# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed for this utility function

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
    Consume the current token from parser_state and advance the position pointer.
    
    Args:
        parser_state: Parser state dictionary containing tokens list and pos pointer
        expected_type: Optional expected token type to validate against
        
    Returns:
        The consumed Token dictionary
        
    Raises:
        SyntaxError: If pos is out of bounds or token type doesn't match expected_type
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if we've reached the end of input
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    # Get the current token
    current_token = tokens[pos]
    
    # Validate token type if expected_type is specified
    if expected_type is not None and current_token["type"] != expected_type:
        raise SyntaxError(
            f"Expected token type '{expected_type}', got '{current_token['type']}'"
        )
    
    # Advance the position pointer
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
