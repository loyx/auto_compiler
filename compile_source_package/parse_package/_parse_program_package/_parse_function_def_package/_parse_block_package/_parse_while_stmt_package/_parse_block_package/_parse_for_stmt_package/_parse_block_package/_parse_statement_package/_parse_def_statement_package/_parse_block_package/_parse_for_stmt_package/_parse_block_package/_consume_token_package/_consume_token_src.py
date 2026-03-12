# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions required for this utility

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
        parser_state: Parser state dictionary containing tokens and current position.
        expected_type: The expected token type (e.g., "COLON", "SEMICOLON", "FOR").
    
    Returns:
        The consumed token dictionary.
    
    Raises:
        SyntaxError: If current token type does not match expected_type or if position is out of bounds.
    
    Side Effects:
        Updates parser_state["pos"] by incrementing it on successful match.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if position is out of bounds
    if pos >= len(tokens):
        raise SyntaxError(
            f"Unexpected end of input. Expected token type '{expected_type}' but no more tokens available."
        )
    
    # Get current token
    current_token = tokens[pos]
    current_type = current_token.get("type")
    
    # Check if token type matches expected type
    if current_type != expected_type:
        raise SyntaxError(
            f"Expected token type '{expected_type}' but got '{current_type}' "
            f"at line {current_token.get('line', '?')}, column {current_token.get('column', '?')}."
        )
    
    # Advance position and return the token
    parser_state["pos"] = pos + 1
    return current_token

# === helper functions ===
# No helper functions needed for this simple utility

# === OOP compatibility layer ===
# Not required - this is a utility function, not a framework entry point