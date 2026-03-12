# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions required

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
def _expect_token(parser_state: ParserState, token_type: str) -> Token:
    """
    Consume a token of expected type from parser state.
    
    Args:
        parser_state: Parser state containing tokens list and current pos
        token_type: Expected token type (e.g., "VAR", "IDENTIFIER", "ASSIGN")
    
    Returns:
        The consumed token
    
    Raises:
        SyntaxError: When token type doesn't match or input ends unexpectedly
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if pos is out of bounds
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input, expected {token_type}")
    
    # Get current token
    current_token = tokens[pos]
    
    # Check if token type matches
    if current_token["type"] != token_type:
        raise SyntaxError(
            f"Expected {token_type}, got {current_token['type']} at line {current_token['line']}"
        )
    
    # Advance position and return token
    parser_state["pos"] += 1
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this helper function