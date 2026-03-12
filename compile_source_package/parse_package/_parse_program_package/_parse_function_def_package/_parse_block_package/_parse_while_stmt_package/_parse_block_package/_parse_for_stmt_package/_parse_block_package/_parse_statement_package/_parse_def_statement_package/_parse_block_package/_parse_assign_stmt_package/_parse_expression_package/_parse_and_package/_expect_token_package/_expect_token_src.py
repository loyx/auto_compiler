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
def _expect_token(parser_state: ParserState, token_type: str) -> Token:
    """
    Consume and validate the current token against expected type.
    
    Args:
        parser_state: Parser state dict containing tokens, pos, filename
        token_type: Expected token type string (e.g., "AND", "EQ", "LPAREN")
    
    Returns:
        The consumed Token if type matches
    
    Raises:
        SyntaxError: If token type doesn't match or end of tokens reached
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # Check if we've reached the end of tokens
    if pos >= len(tokens):
        raise SyntaxError(
            f"Unexpected end of file, expected {token_type} at {filename}"
        )
    
    # Get current token
    current_token = tokens[pos]
    actual_type = current_token["type"]
    
    # Check if token type matches expected
    if actual_type != token_type:
        line = current_token.get("line", "?")
        column = current_token.get("column", "?")
        raise SyntaxError(
            f"Expected {token_type} but got {actual_type} at {filename}:{line}:{column}"
        )
    
    # Consume the token (advance position)
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
