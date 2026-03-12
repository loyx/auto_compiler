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
#   "error": str | None
# }

# === main function ===
def _consume_token(parser_state: ParserState, expected_type: str = None) -> Token:
    """
    Consume current token and advance parser_state["pos"].
    
    If expected_type is provided, validate token type matches.
    Raise SyntaxError on EOF or type mismatch.
    
    Args:
        parser_state: Parser state containing tokens list and pos index
        expected_type: Optional expected token type to validate against
    
    Returns:
        The consumed Token dict
    
    Raises:
        SyntaxError: On EOF or type mismatch
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check for EOF
    if pos >= len(tokens):
        filename = parser_state.get("filename", "unknown")
        raise SyntaxError(f"Unexpected EOF at line {filename}")
    
    # Get current token
    token = tokens[pos]
    
    # Validate type if expected_type is provided
    if expected_type is not None and token["type"] != expected_type:
        raise SyntaxError(
            f"Expected {expected_type} but got {token['type']} "
            f"at line {token['line']}, column {token['column']}"
        )
    
    # Advance position
    parser_state["pos"] = pos + 1
    
    return token

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this utility function