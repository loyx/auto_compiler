# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this utility function

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
    Check and consume a token of expected type from parser state.
    
    Args:
        parser_state: Parser state dict with tokens, pos, filename
        token_type: Expected token type string (e.g., "PLUS", "MINUS", "EQ")
    
    Returns:
        The matched token dict
    
    Raises:
        SyntaxError: If token type doesn't match or position is out of range
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # Check if position is out of range
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:EOF: expected {token_type}, got EOF")
    
    # Get current token
    current_token = tokens[pos]
    actual_type = current_token.get("type", "UNKNOWN")
    
    # Check if token type matches
    if actual_type != token_type:
        line = current_token.get("line", "?")
        column = current_token.get("column", "?")
        raise SyntaxError(
            f"{filename}:{line}:{column}: expected {token_type}, got {actual_type}"
        )
    
    # Consume token (advance position)
    parser_state["pos"] = pos + 1
    
    return current_token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function