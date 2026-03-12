# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed

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
def _expect_token(parser_state: ParserState, token_type: str, value: str) -> None:
    """
    Expect current token to match specified type and value.
    
    If matches, consume the token (pos++).
    If not matches, raise SyntaxError.
    
    Resource IO:
    - READ: parser_state["tokens"], parser_state["pos"]
    - WRITE: parser_state["pos"] (increment on match)
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if position is valid
    if pos >= len(tokens):
        raise SyntaxError(f"Expected '{value}' at end of file")
    
    # Get current token
    current_token = tokens[pos]
    
    # Compare token type and value
    if current_token["type"] != token_type or current_token["value"] != value:
        line = current_token.get("line", 0)
        column = current_token.get("column", 0)
        actual_value = current_token["value"]
        raise SyntaxError(f"Expected '{value}' at line {line}, column {column}, got '{actual_value}'")
    
    # Consume token
    parser_state["pos"] += 1

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function node
